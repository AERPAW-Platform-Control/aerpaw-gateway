#!/usr/bin/perl

use Cwd qw( abs_path );
use File::Basename qw( dirname );
use lib dirname(abs_path($0));
use GeniResponse;
use JSON;

# example:
#$VAR1 = bless( {
#                 'code' => 0,
#                 'logurl' => 'https://emulab-www.exogeni.net/spewlogfile.php3?logfile=a4a9c3f6d3d1ce4b217535bb3727fa24',
#                 'value' => {'uuid' => '4015987d-0980-11eb-a596-6cae8b3bf14a','approved' => '1','idx' => '28'},
#                 'output' => ''
#               }, 'GeniResponse' );

my $read_str = `cat $ARGV[0]`;
my $metadata = eval($read_str);
#print $read_str;
#print $metadata;

my $jsoncoder = JSON::XS->new;
$jsoncoder->convert_blessed(1);
print $jsoncoder->encode($metadata);



