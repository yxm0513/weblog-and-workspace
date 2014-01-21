#!/usr/bin/perl
use Capture::Tiny qw(tee);

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
    if($out=~ /BMC IP SPA: ([\d\.]+)/g){
       $spaip = $1;
       push @ip, $1;
    }
    if($out=~ /BMC IP SPB: ([\d\.]+)/g){
       $spbip = $1;
       push @ip, $1;
    }
}

my $cmd = "ipmitool -I lanplus -H  $spaip  -U admin -P password -C 3 chassis bootdev pxe";
print "CMD: " . $cmd . "\n";
$out = tee {system($cmd)};

sleep 2;
$cmd = "ipmitool -I lanplus -H  $spbip  -U admin -P password -C 3 chassis bootdev pxe";
print "CMD: " . $cmd . "\n";
$out = tee {system($cmd)};
sleep 10;
$cmd = "ipmitool -I lanplus -H  $spaip  -U admin -P password -C 3 chassis power cycle";
print "CMD: " . $cmd . "\n";
$out = tee {system($cmd)};
$cmd = "ipmitool -I lanplus -H  $spbip  -U admin -P password -C 3 chassis power cycle";
print "CMD: " . $cmd . "\n";
$out = tee {system($cmd)};
print "OK.";
