<?
foreach ($argv as $arg) {
	if(preg_match("/\=/", $arg)){
		$e=explode("=",$arg);
	${$e[0]} = $e[1];
	};
};

// splitAuthors.php
// creadted by Jasuk Koo
// 2022.2.14

// this file is encoded by UTF-8 to deal Korean languge.

if(!isset($debug)) $debug = 0;
if($debug) echo "\nDEBUG MODE \n\n";

$progPath = dirname(__FILE__);
include_once("$progPath/mySplitAuthorLib.php"); //load library

//default values
if($debug) echo "input=$bulkfile\n";
if(!isset($input)) $input = "Authors.txt";//default inputfile

$oFilename = "AuthorListOut.txt"; // result out file 1
$o2Filename = "AuthorsOut.txt"; // result out file 2

$lno = 1; // initial value of AuthorList line

// results
$rst = array(); // format 1 : one author info per line
$rst2 = array(); // format 2 : authos for on paper line

$AfilliationNormList = getAfilliationNormList();
$NameNormList = getNameNormList();
$GeneralNormList = getGeneralNormList();

$fp = @fopen($input, "r");
if(!$fp){
	echo "file open error : $input "; exit;
	
}else{
	while (($line =fgets($fp, 4096)) !== FALSE) {
		if(trim($line) == "") continue; // blank line
		if(preg_match("/^\#/", trim($line))) continue; // comment line (# )
			
		// remove some words
		foreach($GeneralNormList as $k => $v){ $line = str_replace($k, $v, $line);}
		
		//default value in line
		$afilliation = "None";
		$rst2[$lno] = "$lno|";
		
		// split author line with comma
		$Authors = preg_split("/,/", trim($line));
		// for each author by backward direction because of affilation search
		for($i=count($Authors)-1; $i >=0; $i--){
			// default value in author
			$isCorrespondingAuthor = FALSE;
			$author = trim($Authors[$i]);
			// parsing ( ) that is afilliation
			if(preg_match("/(.*)\((.*)\)/", $author, $match)){
				$name = trim($match[1]);
				$afilliation = trim($match[2]);
			}else{
				$name = trim($author);
				// afilliation is set to previous value
			};
			
			// parsing * that is corresponding author
			if(preg_match("/(.*)\*/", $author, $match)){
				$name = trim($match[1]);
				$isCorrespondingAuthor = TRUE;
			};
			
			// normalization (afilliation, name)
			if(array_key_exists($afilliation, $AfilliationNormList)){ $afilliation = $AfilliationNormList[$afilliation];}
			if(array_key_exists($name, $NameNormList)){ $name = $NameNormList[$name];}
			// result lines
			$rst[$lno][$i] = "$lno|$name|$afilliation|$isCorrespondingAuthor\n";
			$rst2[$lno] .= "$name($afilliation), ";
		};
		$rst2[$lno] = substr($rst2[$lno],0,-2). "\n";
		$lno++;
	};
	if($fp) fclose($fp);
	
	// print out rst
	$ofp = @fopen($oFilename, "w");
	if(!$ofp){
		echo "file open error : $2Filename "; exit;
	}else{
		// title line
		fputs($ofp, "lnl|name|afilliation|isCorresponding\n");
		foreach($rst as $k=>$v){
			for ($i=0; $i<count($v); $i++){
				fputs($ofp, $v[$i]);
			};
		};
		if(!$ofp) fclose($ofp);
	};
	
	$ofp2 = @fopen($o2Filename, "w");
	if(!$ofp2){
		echo "file open error : $o2Filename "; exit;
	}else{
		// title line
	fputs($ofp2, "no|authors\n");
		foreach($rst2 as $k){
			fputs($ofp2, $k);
		};
		if(!$ofp2) fclose($ofp2);
	};
};
?>