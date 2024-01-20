{
  description = "Build a cargo project with a custom toolchain";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

    crane = {
      url = "github:ipetkov/crane";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    flake-utils.url = "github:numtide/flake-utils";

    rust-overlay = {
      url = "github:oxalica/rust-overlay";
      inputs = {
        nixpkgs.follows = "nixpkgs";
        flake-utils.follows = "flake-utils";
      };
    };
  };

  outputs = { self, nixpkgs, crane, flake-utils, rust-overlay, ... }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ (import rust-overlay) ];
        };

        inherit (pkgs) lib;

        rustOxalica = pkgs.rust-bin.stable.latest.default.override {
          #targets = [ "wasm32-wasi" ];
        };

        # NB: we don't need to overlay our custom toolchain for the *entire*
        # pkgs (which would require rebuidling anything else which uses rust).
        # Instead, we just want to update the scope that crane will use by appending
        # our specific toolchain there.
        craneLib = (crane.mkLib pkgs).overrideToolchain rustOxalica;

        commonArgs = {
          src = ./.;

          buildInputs = with pkgs; [
            llvmPackages_13.libclang
            llvmPackages_13.libcxxClang
          ] ++ lib.optionals stdenv.isDarwin [
            darwin.apple_sdk.frameworks.Security
          ];

          # Extra inputs can be added here
          nativeBuildInputs = with pkgs; [
            clang_13

            rustOxalica
          ];

          LIBCLANG_PATH = "${pkgs.llvmPackages_13.libclang.lib}/lib";
        };

        # Build *just* the cargo dependencies, so we can reuse
        # all of that work (e.g. via cachix) when running in CI
        cargoArtifacts = craneLib.buildDepsOnly (commonArgs // {
          # Additional arguments specific to this derivation can be added here.
          # Be warned that using `//` will not do a deep copy of nested
          # structures
          version = "dev";
        });

        # Run clippy (and deny all warnings) on the crate source,
        # resuing the dependency artifacts (e.g. from build scripts or
        # proc-macros) from above.
        #
        # Note that this is done as a separate derivation so it
        # does not impact building just the crate by itself.
        mastiffClippy = craneLib.cargoClippy (commonArgs // {
          # Again we apply some extra arguments only to this derivation
          # and not every where else. In this case we add some clippy flags
          inherit cargoArtifacts;
          cargoClippyExtraArgs = "-- --deny warnings";
        });

        # Check formatting
        mastiffFmt = craneLib.cargoFmt (commonArgs // {
          inherit cargoArtifacts;
        });

        # Run tests with cargo-nextest
        # Consider setting `doCheck = false` on `my-crate` if you do not want
        # the tests to run twice
        mastiffNextest = craneLib.cargoNextest (commonArgs // {
          inherit cargoArtifacts;
          partitions = 1;
          partitionType = "count";
        } // lib.optionalAttrs (system == "x86_64-linux") {
          # NB: cargo-tarpaulin only supports x86_64 systems
          # Check code coverage (note: this will not upload coverage anywhere)
          #mastiffCoverage = craneLib.cargoTarpaulin (commonArgs // {
          #  inherit cargoArtifacts;
          #});
        });

        # Build the actual crate itself, reusing the dependency
        # artifacts from above.
        mastiff-server = craneLib.buildPackage (commonArgs // {
          inherit cargoArtifacts;
          src = ./.;
          pname = "mastiff-server";
          cargoExtraArgs = "--bin mastiff-server";
        });

        # Build the actual crate itself, reusing the dependency
        # artifacts from above.
        mastiff-client = craneLib.buildPackage (commonArgs // {
          inherit cargoArtifacts;
          src = ./.;
          pname = "mastiff-client";
          cargoExtraArgs = "-p mastiff-client --bin mastiff-client";
        });
      in
      {
        packages.default = mastiff-server;
        packages.mastiff-server = mastiff-server;
        packages.mastiff-client = mastiff-client;

        apps.default = flake-utils.lib.mkApp {
          drv = mastiff-server;
        };

        checks = {
         inherit
           # Build the crate as part of `nix flake check` for convenience
           mastiff-server
           mastiff-client
           mastiffFmt
           mastiffClippy
           mastiffNextest;
        };

        devShells.default = pkgs.mkShell (commonArgs // {
          inputsFrom = builtins.attrValues self.checks;

          buildInputs = with pkgs; [
              oha
              #awscli2
              rclone
              nixpkgs-fmt
              asciinema
              asciinema-agg

              cargo-udeps
              cargo-outdated
              cargo-watch
              cargo-limit

              snakemake
              parallel-full
          ];
        });
      });
}

