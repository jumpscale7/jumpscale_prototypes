class { 'ntp':
    servers => [ 'pool.ntp.org '],
  }

 notify {$::ipaddress:}