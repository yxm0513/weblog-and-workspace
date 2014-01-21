#!/usr/bin/perl
use Capture::Tiny qw(tee);
use File::Copy;

##################################################################
# Exit Code
# 0 : success
# 1 : fail
# 2 : sp is not pingable 
# 3 : rescue mode
# 4 : incomplete collection


if($#ARGV < 0){
    print("usage: $0 host [ar].\n");
    exit(1);
}

sub getARFolder {
    $ARGV[1] =~ s/^\s*//;
    $ARGV[1] =~ s/\s*$//;
    $cmd = "/c4shares/auto/devutils/bin//whereisAR $ARGV[1]";
    $out = `$cmd`;
    print "CMD: " . $cmd . "\r\n";
    if($out =~ /not found/){
      print "ERROR:" . $out . "\r\n";
      exit 1;
    }else{
      $out =~ /([\/\d\w_-]+)/g;
      my $folder = $1;
      return $folder;
    }
}

##################################################################
#  get system ip 
##################################################################
my @ip;
my $sys;
my $spaip;
my $spbip;
my $cmd = '/c4shares/auto/devutils/bin/swarm ' . $ARGV[0];
print "CMD: " . $cmd . "\n";
my $out = `$cmd`;
if( $out=~ /Can't find system/){
   print "ERROR: Can't find system"  .  $ARGV[0]  . "\n";   
} else {
    if($out=~ /Lab IP SPA: ([\d\.]+)/g){
       $spaip = $1;
       push @ip, $1;    
    }
    if($out=~ /Lab IP SPB: ([\d\.]+)/g){
       $spbip = $1;
       push @ip, $1;    
    }
}

##################################################################
#  check system is pingable
##################################################################
foreach my $ip (@ip){
    unless(system("ping -c 1 ". $ip ) == 0 ){
        print("ERROR: ". $ip . " is not pingable\n");   
        exit 2;
    }
}
$sys = $ip[0];
unless ($sys){
    print("ERROR: cannot get system ip\n");
    exit 1;    
}
##################################################################
#  check service mode 
##################################################################
foreach my $ip (@ip){
    #/sbin/get_boot_mode
    $cmd = 'ssh -o "StrictHostKeyChecking no" root@' . $ip . ' /sbin/get_boot_mode ';
    print "CMD: " . $cmd . "\n";
    $out = tee {system($cmd)};
    if($out =~ /Rescue Mode/g){
        print "WARN: system $ip in Rescue Mode\n";
        #exit 3;
    }
}
##################################################################
#  do svc_dc 
##################################################################
$cmd = 'ssh -o "StrictHostKeyChecking no" root@' . $sys . ' svc_dc ';
print "\nCMD: " . $cmd . "\n";
$out = tee {system($cmd)};
# if match ERROR

#if($out =~ /incomplete collection/g){
#    exit 4;    
#}

if ($ARGV[1]){
    # svc_dc
    my $file;
    if($out =~ /collected at (\/\S+tar)/g){
       $file = $1;
    }else{
       print "Error: NO file generated";
       exit 1;
    }
    my $folder = getARFolder();
    $cmd = 'scp -o "StrictHostKeyChecking no" root@' . $sys . ':'.$file . "  $folder";
    print "CMD: " . $cmd . "\n";
    $out = tee {system($cmd)};
}
##################################################################
#  do triage command 
##################################################################
$cmd = 'bash /c4shares/auto/devutils/bin//triage ' . $ARGV[0];
print "CMD: " . $cmd . "\n";
$out = tee {system($cmd)};
##################################################################
#  do copys 
##################################################################
if ($ARGV[1]){
    # triage
    $file = $ARGV[0] . "\.out";
    my $folder = getARFolder();
    $cmd = "cp $file $folder";
    print "CMD: " . $cmd . "\n";
    $out = tee {system($cmd)};
##################################################################
#  scp cores command 
##################################################################
if($spaip){
    my $path = $folder."/spacores/cores/";
    $cmd = "mkdir -p $path";
    print "CMD: " . $cmd . "\n";
    $out = tee {system($cmd)};
    $cmd = "scp -r root@" . $spaip . ":/cores $path";
    print "CMD: " . $cmd . "\n";
    $out = tee {system($cmd)};
    my $backendpath = $folder."/spacores/backend/";
    $cmd = "mkdir -p $backendpath";
    print "CMD: " . $cmd . "\n";
    $out = tee {system($cmd)};
    $cmd = "scp -r root@".$spaip.":/EMC/backend/service/data_collection/cores $backendpath";
    print "CMD: " . $cmd . "\n";
    $out = tee {system($cmd)};
}
if($spbip){
    my $path = $folder."/spbcores/cores/";
    $cmd = "mkdir -p $path";
    print "CMD: " . $cmd . "\n";
    $out = tee {system($cmd)};
    $cmd = "scp -r root@" . $spbip . ":/cores $path";
    print "CMD: " . $cmd . "\n";
    $out = tee {system($cmd)};
    my $backendpath = $folder."/spbcores/backend/";
    $cmd = "mkdir -p $backendpath";
    print "CMD: " . $cmd . "\n";
    $out = tee {system($cmd)};
    $cmd = "scp -r root@".$spbip.":/EMC/backend/service/data_collection/cores $backendpath";
    print "CMD: " . $cmd . "\n";
    $out = tee {system($cmd)};
}
}
