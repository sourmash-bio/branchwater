{
  description = "Deploy a full system with hello service as a separate profile";

  inputs.deploy-rs.url = "github:serokell/deploy-rs";
  inputs.branchwater.url = "github:sourmash-bio/branchwater";

  outputs = { self, nixpkgs, deploy-rs, branchwater }: {

    nixosModule = { config, lib, pkgs, ... }:
      with lib;
      let cfg = config.branchwater.services.api;
      in {
        options.branchwater.services.api = {
          enable = mkEnableOption "Enables the branchwater HTTP API service";

          domain = mkOption rec {
            type = types.str;
            default = "/scratch";
            example = default;
            description = "Location of the branchwater DB to serve";
          };
        };

        config = mkIf cfg.enable {
          systemd.services."branchwater.api" = {
            wantedBy = [ "multi-user.target" ];

            serviceConfig =
              let pkg = branchwater.packages.${pkgs.system}.default;
              in {
                Restart = "on-failure";
                ExecStart = "${pkg}/bin/branchwater-server -k21 /scratch";
                DynamicUser = "yes";
                RuntimeDirectory = "branchwater.api";
                RuntimeDirectoryMode = "0755";
                StateDirectory = "branchwater.api";
                StateDirectoryMode = "0700";
                CacheDirectory = "branchwater.api";
                CacheDirectoryMode = "0750";
              };
          };
        };
      };

    nixosConfigurations = {
      branchwater-sourmash-bio = nixpkgs.lib.nixosSystem {
        system = "aarch64-linux";
        modules = [
          self.nixosModule
          ./configuration-aarch64.nix
        ];
      };

      branchwater-sourmash-bio_x86 = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          self.nixosModule
          ./configuration.nix
        ];
      };
    };

    # This is the application we actually want to run
    #defaultPackage.x86_64-linux = import ./hello.nix nixpkgs;

    deploy.nodes."branchwater" = {
      sshOpts = [ "-p" "22" "-i" "~/.aws/Luiz-sourmash.pem" ];
      hostname = "branchwater.sourmash.bio";
      fastConnection = false;
      profiles = {
        system = {
          sshUser = "root";
          path =
            deploy-rs.lib.aarch64-linux.activate.nixos self.nixosConfigurations.branchwater-sourmash-bio;
          user = "root";
        };
      };
    };

    checks = builtins.mapAttrs (system: deployLib: deployLib.deployChecks self.deploy) deploy-rs.lib;
  };
}
