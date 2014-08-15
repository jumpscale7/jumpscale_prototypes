user { 'katie':
  ensure => 'present',
  home   => '/home/katie',
  shell  => '/bin/zsh'
}

#user {'katie':
#      ensure => absent,
#}