{ modulesPath, pkgs, ... }: {
  imports = [ "${modulesPath}/virtualisation/amazon-image.nix" ];
  ec2.hvm = true;
  ec2.efi = true;
  networking.hostName = "branchwater";
  system.stateVersion = "22.05";

  fileSystems."/scratch" =
    {
      device = "/dev/nvme1n1";
      fsType = "ext4";
      options = [ "rw" "relatime" ];
    };

  nix = {
    extraOptions = ''
      experimental-features = nix-command flakes
    '';
    gc = {
      automatic = true;
      dates = "weekly";
      options = "--delete-older-than 30d";
    };
    extraOptions = ''
      min-free = ${toString (100 * 1024 * 1024)}
      max-free = ${toString (1024 * 1024 * 1024)}
    '';
  };

  environment = {
    systemPackages = with pkgs; [
      wget
      vim
      git
      tmux
      htop
    ];
  };

  services.caddy = {
    enable = true;
    email = "luiz@sourmash.bio";
    virtualHosts."branchwater.sourmash.bio".extraConfig = ''
      reverse_proxy http://127.0.0.1:3059
    '';
  };

  services.datadog-agent = {
    enable = true;
    enableLiveProcessCollection = true;
    enableTraceAgent = true;
    tags = [ "branchwater" ];
    apiKeyFile = "/var/log/datadog/ddagent.key";
    extraConfig = {
      logs_enabled = true;
    };
    checks = {
      "journal" = {
        logs = {
          type = "journald";
        };
      };
      "caddy" = {
        logs = {
          type = "file";
          path = "/var/log/caddy/access-branchwater.sourmash.bio.log";
          service = "branchwater";
          source = "caddy";
        };
      };
    };
  };
  users.users.datadog = {
    group = "datadog";
    extraGroups = [ "systemd-journal" ];
    isSystemUser = true;
  };
  users.groups.datadog = { };

  branchwater.services.api.enable = true;

  networking.firewall = {
    enable = true;
    interfaces.ens5 = {
      allowedTCPPorts = [ 80 443 ];
    };
  };
}
