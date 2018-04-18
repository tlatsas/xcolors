#!/usr/bin/perl -w
use strict;
use warnings;
use Path::Tiny;
use LWP::UserAgent;

=explain
  I use KiTTY w/ SuperPuTTY in Win10, and have found a reliable 
  way to impose color themes on my SSH sessions!

  (I'm not sure how applicable this is for anyone else...)  

  Unfortunately, it involves importing a list of British RGB 'colours'
  via Regedit:
  0. Run this via CLI and add the URL as an argument, or just edit inline below
  1. Import the result via Regedit.exe
  2. Enjoy!

  - e-n-l
=cut

my $file       = "Windows Registry Editor Version 5.00\n\n" .
                 '[HKEY_CURRENT_USER\Software\9bis.com\KiTTY\Sessions\Default%20Settings]' . "\n";
my $url        = $ARGV[0] || 'http://www.xcolors.net/dl/sourcerer';
my $bold_delta = 10; # quick / dirty "bold" color darken adjustment



my $ua = LWP::UserAgent->new;
my $res = $ua->get($url);
my $string = '';

$string = ($res->is_success) ? $res->decoded_content : die $res->status_line;

$string =~ s/\n\!.*\n/\n/g;

my $input = {};
foreach(split /\n/, $string){
  $_ =~ m/\*\.?([^:]*):\s*\#([\w\d]*)/;
  next unless $1 and $2;
  $input->{$1} = de_hex($2);
  $input->{"_${1}"} = bold($input->{$1});
}

$input->{cursorColor} ||= $input->{color2};
$input->{borderColor} ||= $input->{background};

my @map = (
  'foreground',  # "Colour0",  # 187,187,0      # Default Foreground
  '_foreground', # "Colour1",  # 255,255,1      # Default Bold Foreground
  'background',  # "Colour2",  # 0,0,0          # Default Background
  '_background', # "Colour3",  # 85,85,85        # Default Bold Background
  'borderColor', # "Colour4",  # 0,0,0          # Cursor Text
  'cursorColor', # "Colour5",  # 0,255,0        # Cursor Color
  'color0',      # "Colour6",  # 0,0,0          # ANSI Black
  'color8',      # "Colour7",  # 85,85,85       # ANSI Black Bold
  'color1',      # "Colour8",  # 187,0,0        # ANSI Red
  'color9',      # "Colour9",  # 255,85,85      # ANSI Red Bold
  'color2',      # "Colour10", # 0,187,0        # ANSI Green
  'color10',     # "Colour11", # 85,255,11      # ANSI Green Bold
  'color3',      # "Colour12", # 187,187,0      # ANSI Yellow
  'color11',     # "Colour13", # 255,255,13     # ANSI Yellow Bold
  'color4',      # "Colour14", # 0,0,187        # ANSI Blue
  'color12',     # "Colour15", # 85,85,15       # ANSI Blue Bold
  'color5',      # "Colour16", # 187,0,187      # ANSI Magenta
  'color13',     # "Colour17", # 255,85,17      # ANSI Magenta Bold
  'color6',      # "Colour18", # 0,187,187      # ANSI Cyan
  'color14',     # "Colour19", # 85,255,19      # ANSI Cyan Bold
  'color7',      # "Colour20", # 187,187,187    # ANSI White
  'color15',     # "Colour21", # 255,255,255    # ANSI White Bold
  'foreground',  # "Colour22", # 187,187,187    # 0
  'background',  # "Colour23", # 0,0,0          # 2
  '_background', # "Colour24", # 0,0,0          # 2
  'color1',      # "Colour25", # 187,0,0        # 8
  'color2',      # "Colour26", # 0,187,0        # 10
  'color3',      # "Colour27", # 187,187,0      # 12
  'color4',      # "Colour28", # 0,0,187        # 14
  'color5',      # "Colour29", # 187,0,187      # 16
  'color6',      # "Colour30", # 0,187,187      # 18 
  'color7',      # "Colour31", # 187,187,187    # 0
  'background',  # "Colour32", # 0,0,0          # 2
  'foreground',  # "Colour33", # 187,187,187    # 0
);

my %result = ();
foreach(0..33){
  my $value = $input->{ $map[$_] };
  $result{"Colour$_"} = $value;
  $file .= "\"Colour$_\"=\"$value\"\n";
}

## print to STDOUT:
print $file;

## or dump to file:
# open my $fh, '>', 'kitty_clrs.reg'; print $fh $file; close $fh;

sub bold {
  my @clr = split ',', shift;
  return join ',', map { $_ = ($_ >= $bold_delta) ? $_ - $bold_delta : 0 } @clr;
}

sub de_hex {
  my $hexed = uc shift;
  my @deced;
  my %h2d = (
    0 => 0,
    1 => 1,
    2 => 2,
    3 => 3,
    4 => 4,
    5 => 5,
    6 => 6,
    7 => 7,
    8 => 8,
    9 => 9,
    A => 10,
    B => 11,
    C => 12,
    D => 13,
    E => 14,
    F => 15,
  );
  my $digit = 0;
  foreach(0..5){
    $digit = $digit + $h2d{ (split '', $hexed)[$_] };
    unless ($_ % 2){      
      $digit *= 16;
    } else {
      push @deced, $digit;
      $digit = 0;
    }
  }
  return join ',', @deced;
}
