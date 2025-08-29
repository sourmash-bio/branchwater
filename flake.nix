{
  description = "Build a cargo project with a custom toolchain";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

    crane = {
      url = "github:ipetkov/crane";
    };

    flake-utils.url = "github:numtide/flake-utils";

    rust-overlay = {
      url = "github:oxalica/rust-overlay";
      inputs = {
        nixpkgs.follows = "nixpkgs";
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

        inherit (pkgs) lib stdenv;

        rustOxalica = pkgs.rust-bin.stable.latest.default.override {
          #targets = [ "wasm32-wasi" ];
          extensions = ["llvm-tools-preview"];
        };

        # NB: we don't need to overlay our custom toolchain for the *entire*
        # pkgs (which would require rebuidling anything else which uses rust).
        # Instead, we just want to update the scope that crane will use by appending
        # our specific toolchain there.
        craneLib = (crane.mkLib pkgs).overrideToolchain rustOxalica;

        commonArgs = {
          src = ./.;
          preConfigure = lib.optionalString stdenv.isDarwin ''
            export MACOSX_DEPLOYMENT_TARGET=10.14
          '';

          buildInputs = with pkgs; [
            llvmPackages_16.libclang
            llvmPackages_16.libcxxClang
          ];

          # Extra inputs can be added here
          nativeBuildInputs = with pkgs; [
            clang_16

            rustOxalica
          ];

          LIBCLANG_PATH = "${pkgs.llvmPackages_16.libclang.lib}/lib";
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
        branchwaterClippy = craneLib.cargoClippy (commonArgs // {
          # Again we apply some extra arguments only to this derivation
          # and not every where else. In this case we add some clippy flags
          inherit cargoArtifacts;
          cargoClippyExtraArgs = "-- --deny warnings";
        });

        # Check formatting
        branchwaterFmt = craneLib.cargoFmt (commonArgs // {
          inherit cargoArtifacts;
        });

        # Run tests with cargo-nextest
        # Consider setting `doCheck = false` on `my-crate` if you do not want
        # the tests to run twice
        branchwaterNextest = craneLib.cargoNextest (commonArgs // {
          inherit cargoArtifacts;
          partitions = 1;
          partitionType = "count";
        } // lib.optionalAttrs (system == "x86_64-linux") {
          withLlvmCov = true;
          # NB: cargo-tarpaulin only supports x86_64 systems
          # Check code coverage (note: this will not upload coverage anywhere)
          #branchwaterCoverage = craneLib.cargoLlvmCov (commonArgs // {
          #  inherit cargoArtifacts;
          #});
        });

        # Build the actual crate itself, reusing the dependency
        # artifacts from above.
        branchwater-server = craneLib.buildPackage (commonArgs // {
          inherit cargoArtifacts;
          src = ./.;
          pname = "branchwater-server";
          cargoExtraArgs = "--bin branchwater-server";
        });

        # Build the actual crate itself, reusing the dependency
        # artifacts from above.
        branchwater-client = craneLib.buildPackage (commonArgs // {
          inherit cargoArtifacts;
          src = ./.;
          pname = "branchwater-client";
          cargoExtraArgs = "-p branchwater-client --bin branchwater-client";
        });

        # Build the actual crate itself, reusing the dependency
        # artifacts from above.
        branchwater-query = craneLib.buildPackage (commonArgs // {
          inherit cargoArtifacts;
          src = ./.;
          pname = "branchwater-query";
          cargoExtraArgs = "-p branchwater-query --bin branchwater-query";
        });
      in
      {
        packages.default = branchwater-server;
        packages.branchwater-server = branchwater-server;
        packages.branchwater-client = branchwater-client;
        packages.branchwater-query = branchwater-query;

        apps.default = flake-utils.lib.mkApp {
          drv = branchwater-server;
        };

        checks = {
          inherit
            # Build the crate as part of `nix flake check` for convenience
            branchwater-server
            branchwater-client
            branchwaterFmt
            branchwaterClippy
            branchwaterNextest;
        };

        devShells.default = pkgs.mkShell.override { } (commonArgs // {
          inputsFrom = builtins.attrValues self.checks;

          buildInputs = with pkgs; [
            oha
            #awscli2
            rclone
            nixpkgs-fmt
            asciinema
            asciinema-agg

            cargo-deny
            cargo-udeps
            cargo-outdated
            cargo-watch
            cargo-limit
            rust-analyzer

            snakemake
            parallel-full
            pixi

            podman-compose

            (python311.withPackages (ps: with ps; [
              furo
              myst-parser
              sphinx
              sphinx-copybutton
              sphinx-design
              sphinx-inline-tabs
              sphinx-tabs
              sourmash
              tox
            ]))
          ];
          shellHook = ''
            export MACOSX_DEPLOYMENT_TARGET=10.14
          '';
        });
      });
}

