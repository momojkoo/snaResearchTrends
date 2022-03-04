# snaResearchTrends
Social Network Analysis for Research Trends

학술대회 논문제목/저자 목록 데이터를 정리하여 SNA를 수행하기 위한 파일들

## Files
| Category | Filename | Descriptions |
|---|---|---|
| [Authors](#authors)  	| splitAuthors.php 		| main process		|
|						| mySplitAuthorLib.php	| functions			|
|						| splitAuthors_run.bat 	| batch run			|
|						| Authors.txt 			| (example input)	|
| [Titles](#titles)  	| sna.py 				| main process		|
|						| VocabDict.py 			| data class		|
|						| sna_run.bat 			| batch run			|
|						| userDict.txt 			| user dictionary	|
|						| userStopWords.txt 	| user stopwords	|
|						| Titles.txt 			| (example input)	|
| [EdgeList](#edge-list)| myNetworkAnalysis.py 	| main process		|
|						| myNetworkAnalysis_run.bat | batch run		|
|						| EdgeTest.txt 			| (example input)	|
| etc					| deleteOutputs.bat 	| 					|

## Authors
발표논문의 저자목록 형식을 표준화한다.
* 소속명칭 중 불필요한 단어 삭제, 풀어써서 긴 단어를 축약형으로 통일
* 모든 저자들에 소속을 표시 - 저자목록을 뒤에서 부터 읽어와서, 소속이 없는 저자는 뒷 저자의 소속과 동일하도록 지정한다
* 저자명, 저자의 소속을 표준화 - 다양하게 표현된 명칭을 하나로 통일한다
* 교신 저자임을 표시

### input format (Authors.txt : default input filename)
```
이대훈*, 변찬(UNIST)
김지혜*, 김종성(영남대), 박거호(인성이엔지), 한정우(전진인더스), 김진호(영남대)
안형준*(숭실대)
```

### output format1 (AuthorsOut.txt)
```
no|authors
1|변찬(울산과학기술원), 이대훈(울산과학기술원)
2|김진호(영남대), 한정우(전진인더스), 박거호(인성이엔지), 김종성(영남대), 김지혜(영남대)
3|안형준(숭실대)
```


### output format2 (AuthorsListOut.txt)
```
lnl|name|afilliation|isCorresponding
1|이대훈|울산과학기술원|1
1|변찬|울산과학기술원|
2|김지혜|영남대|1
2|김종성|영남대|
2|박거호|인성이엔지|
2|한정우|전진인더스|
2|김진호|영남대|
3|안형준|숭실대|1
```

### 표준화 방식 (mySplitAuthorLib.php)
1. 일반단어 표준화 (function getGeneralNormList)
```
		"주식회사"	=> "",
		"㈜"	=> "",
		"(주)"	=> "",
		", Inc)"	=> "",
		"(재)"	=> "",
		"대학교"	=> "대",
```
1. 단체명 표준화 (function getAfilliationNormList)
```
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
```

1. 인명 표준화 (function getNameNormList)
```
		"Sang-Jae Kim"	=> "김상재",
```


## Titles
발표논문의 제목에서 형태소분석을 하여 단어를 추출한다.
* 사용자 사전의 정의 - 기존 한글 사전에 없는 기술용어, 전문용어, 외래어 등 정의 (단어, 품사, 우선순위)
* 사용자 제외어 정의 - 빈도가 많아서 분석에 활용할 수 없는 단어 제외
* 선정을 위한 품사 결정 : 여기서는 체언(NNG, NNP, NP)과 외래어(SL)만 사용함
* 형태소 분석 수행하여 의미 단어들을 추출 (점검 : morphemeOut.txt)
*. 추출된 단어들의 빈도수 출력 (frequencyOut.txt)
*. 특정 빈도수 이상 나오는 단어로 필터링 (vThreshold = 10)
*. 논문제목에 동시에 출연하는 단어쌍 추출하여 빈도수 계산

### input format (Titles.txt : default input filename)
```
수소충전소 신뢰성 향상을 위한 운전데이터 분석 시스템 연구
가속수명 시험을 적용한 볼베어링의 그리스 주입 주기 신뢰성 평가에 관한 연구
6.6kV 회전기 절연시스템 열적열화 시간에 따른 부분방전 및 절연저항 변화에 대한 고찰
배선용 저압차단기의 부품간섭 및 오동작 원인규명을 위한 공차분석
```
한 줄마다 논문 제목을 표시

### output format1 (morphemeOut.txt)
```
============================
수소충전소 신뢰성 향상을 위한 운전데이터 분석 시스템 연구
>> 수소충전소, 신뢰성, 향상, 운전, 데이터, 분석, 시스템, 연구
============================
가속수명 시험을 적용한 볼베어링의 그리스 주입 주기 신뢰성 평가에 관한 연구
>> 가속수명, 시험, 적용, 볼베어링, 그리스, 주입, 주기, 신뢰성, 평가, 연구
============================
6.6kV 회전기 절연시스템 열적열화 시간에 따른 부분방전 및 절연저항 변화에 대한 고찰
>> kv, 회전기, 절연, 시스템, 열, 시간, 부분, 방전, 절연, 저항, 변화, 고찰
============================
배선용 저압차단기의 부품간섭 및 오동작 원인규명을 위한 공차분석
>> 배선, 저압차단기, 부품, 간섭, 오동작, 원인, 규명, 공차분석
```
형태소 분석이 제대로되었는지 확인하기 위한 출력    
각 라이별로 추출된 형태소를 보여줌

### output format2 (frequencyOut.txt)
```
수소충전소|1
신뢰성|2
향상|1
운전|1
데이터|1
분석|1
시스템|2
연구|2
가속수명|1
시험|1
...
```
단어별 빈도수 출력

### output format3 (cofrequencyOut.txt)
```
신뢰성|시스템|2|2|1|250.000000
신뢰성|연구|2|2|2|500.000000
시스템|연구|2|2|1|250.000000
시스템|절연|2|2|1|250.000000
```
단어1, 단어2, 단어1의 빈도수, 단어2의 빈도수, 점수    
점수 = 동시발생 회수 / (단어1 빈도수 * 단어2 빈도수) * 1000


## Edge list
Node, Edge 등을 SNA 분석을 위한 형식으로 변환한다.(tgf, csv)    
tgf : [trivial graph format](https://en.wikipedia.org/wiki/Trivial_Graph_Format)    
tgf 파일을 yED 의 입력으로, csv 파일은 gephi 의 입력으로 사용한다.

* read input str
* get pair
* get node list
* get adjacency matrix
* get AutoList(x)
* get Autolist(y)


### input format (EdgeTest.txt)
```
1|a,b,c
2|a,b,d
3|b,c,d,e
```

### output format1 (0_Edges.tgf)
```
#
1 a
1 b
1 c
2 a
2 b
2 d
3 b
3 c
3 d
3 e
```

### output format2 (0_Edges_A.tgf, 1_Edges_A.csv)
```
#
1 2 2
1 3 2
2 1 2
2 3 2
3 1 2
3 2 2
```
```
source, target, weight
1, 2, 2
1, 3, 2
2, 1, 2
2, 3, 2
3, 1, 2
3, 2, 2
```

### output format3 (0_Edges_B.tgf, 1_Edges_B.csv)
```
#
a b 2
a c 1
a d 1
b a 2
b c 2
b d 2
b e 1
c a 1
c b 2
c d 1
c e 1
d a 1
d b 2
d c 1
d e 1
e b 1
e c 1
e d 1
```
```
source, target, weight
a, b, 2
a, c, 1
a, d, 1
b, a, 2
b, c, 2
b, d, 2
b, e, 1
c, a, 1
c, b, 2
c, d, 1
c, e, 1
d, a, 1
d, b, 2
d, c, 1
d, e, 1
e, b, 1
e, c, 1
e, d, 1
```