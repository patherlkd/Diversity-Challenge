#!/usr/bin/perl

use v5.10;

my $image_comm = "mogrify -gravity Center -crop 90%x90%+0+0 -mattecolor DodgerBlue4 -frame 10%x10%+5+5";

my $path = $ARGV[0];

my $reset = $ARGV[1];

opendir(my $dir, $path);

while(my $item = readdir $dir){

	if($item =~ m/^question/){
		say $item;
	

		if($reset==1){
		 say "-> reseting to original image.jpg";
		 system("cp ${item}/backup.jpg ${item}/image.jpg && rm ${item}/backup.jpg");
		} else{
	
			my $check=`ls ${item}/backup.jpg`;
			chomp ${check};

			if($check !~ m/backup/){
				say "-> backing up";		
				system("cp ${item}/image.jpg ${item}/backup.jpg");
				say "-> cropping and adding frame";
				system("${image_comm} ${item}/image.jpg");
			}
		}	
	}	
}

closedir($dir);
