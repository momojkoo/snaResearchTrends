<?
// mySplitAuthorLib
// created by Jasuk Koo
// 2022.2.14
//   function list for Natural language process in processing paper survey

// This file is encoded by UTF-8 to deal Korean language.

//////////////////////
function getGeneralNormList(){
	$arr = array(
		"주식회사"	=> "",
		"㈜"	=> "",
		"(주)"	=> "",
		", Inc)"	=> "",
		"(재)"	=> "",
		"대학교"	=> "대",
	);
	return $arr;
}

function getAfilliationNormList(){
	$arr = array(
		// 학교

		// 연구소
		
		// 산업체

		// 영문 : 학교
		"KAIST"	=> "한국과학기술원",
		"UNIST"	=> "울산과학기술원",
		"GIST"	=> "광주과학기술원",
		"POSTECH"	=> "포항공대",

		// 영문 : 연구소
		"KRISS"	=> "한국과학기술원",

		// 영문 : 산업체
		"POSCO"	=> "포스코",
		"POCSO"	=> "포스코",
	);
	return $arr;
}

function getNameNormList(){
	$arr = array(
		"Sang-Jae Kim"	=> "김상재",
	);
	return $arr;
}
?>