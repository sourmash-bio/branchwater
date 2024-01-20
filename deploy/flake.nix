{
  description = "Deploy a full system with hello service as a separate profile";

  inputs.deploy-rs.url = "github:serokell/deploy-rs";
  inputs.mastiff.url = "github:sourmash-bio/mastiff";

  outputs = { self, nixpkgs, deploy-rs, mastiff }: {

    nixosModule = { config, lib, pkgs, ... }:
      with lib;
      let cfg = config.mastiff.services.api;
      in {
        options.mastiff.services.api = {
          enable = mkEnableOption "Enables the mastiff HTTP service";

          domain = mkOption rec {
            type = types.str;
            default = "/scratch";
            example = default;
            description = "Location of the mastiff DB to serve";
          };
        };

        config = mkIf cfg.enable {
          systemd.services."mastiff.api" = {
            wantedBy = [ "multi-user.target" ];

            serviceConfig =
              let pkg = mastiff.packages.${pkgs.system}.default;
              in {
                Restart = "on-failure";
                ExecStart = "${pkg}/bin/mastiff-server -k21 /scratch";
                DynamicUser = "yes";
                RuntimeDirectory = "mastiff.api";
                RuntimeDirectoryMode = "0755";
                StateDirectory = "mastiff.api";
                StateDirectoryMode = "0700";
                CacheDirectory = "mastiff.api";
                CacheDirectoryMode = "0750";
              };
          };
        };
      };

    nixosConfigurations = {
      mastiff-sourmash-bio = nixpkgs.lib.nixosSystem {
        system = "aarch64-linux";
        modules = [
          self.nixosModule
          ./configuration-aarch64.nix
        ];
      };

      mastiff-sourmash-bio_x86 = nixpkgs.lib.nixosSystem {
        system = "x86_64-linux";
        modules = [
          self.nixosModule
          ./configuration.nix
        ];
      };
    };

    # This is the application we actually want to run
    #defaultPackage.x86_64-linux = import ./hello.nix nixpkgs;

    deploy.nodes."mastiff" = {
      sshOpts = [ "-p" "22" "-i" "~/.aws/Luiz-sourmash.pem" ];
      hostname = "mastiff.sourmash.bio";
      fastConnection = false;
      profiles = {
        system = {
          sshUser = "root";
          path =
            deploy-rs.lib.aarch64-linux.activate.nixos self.nixosConfigurations.mastiff-sourmash-bio;
          user = "root";
        };
      };
    };

    checks = builtins.mapAttrs (system: deployLib: deployLib.deployChecks self.deploy) deploy-rs.lib;
  };
}
