#!/usr/bin/env perl

foreach $infile (@ARGV)
{
	open IN, $infile 
	    	or die "failed to open file $!\n";

	open OUT, ">", $infile.".txt"
		or die "failed to open output file $!\n";
	
	binmode IN;
	
	read IN, $buffer, 5;
	$M1 = unpack ("a5", $buffer); #5 digit ascii length of string of canf file
	# print "M1:\t$M1\n";
	
	read IN, $cnaf, $M1;
	print OUT "CNAF file:\t$cnaf\n";
	
	read IN, $buffer, 5;
	$M2 = unpack ("a5", $buffer); #5 digit ascii length of string of comment
	#print "M2:\t$M2\n";
	
	read IN, $comment, $M2;
	print OUT "comment:\t$comment\n";
	
	read IN, $buffer, 5;
	$M3 = unpack ("a5", $buffer); #number of CAMAC-read parameters per event
	print OUT "CAMAC parameters per event:\t$M3\n";
	
	read IN, $buffer, 5;
	$M4 = unpack ("a5", $buffer); #number of total (incl. calculated) parameters per event
	#print "total number of parameters per event (recorded plus calculated):\t$M4\n";
	
	read IN, $buffer, 5;
	$rec_lang = unpack ("a5", $buffer); #number of events per record
	print OUT "number of events per record:\t$rec_lang\n";
	
	read IN, $buffer, 6;
	$totchan = unpack ("a6", $buffer); #sum of all histogram channels
	#print "totchan:\t$totchan\n";
	
	read IN, $date, 8;
	print OUT "date:\t$date\n";
	
	read IN, $time, 8;
	print OUT "time:\t$time\n";
	
	$read_param=0;
	while ( read (IN, $buffer, 2) ) 
	{
	    $read_param++;
	    $temp = unpack ( "s", $buffer);
		if ( $read_param <= $rec_lang * $M4 )
		{
			print OUT "$temp";
			if ($read_param % $M4 == 0)
			{
				print OUT "\n"; 
			} else {
				print OUT "\t";
			}
	
		}
		if ($read_param == 1024) #every 1024 events we start a new record. One word to be discarded
		{
			#print "$temp\n";# it's a zero
			$read_param = 0;
		}
	}
	close IN;
	close OUT;
}		
