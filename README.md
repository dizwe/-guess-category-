# -guess-category-
문장이나 url을 입력하면 카테고리를 추정합니다(현재 카테고리는  정치, 경제, 사회,생활, 세계, 과학/IT 로 나누어져있습니다)

사용하실때 출처를 밝혀주세요.
문의는 dizwe2716@gmail.com이나 이슈로 남겨주세요.


Documents
-------------
>NOTE
-------------

    ● 아직은 한글 문장,글 만을 지원합니다.

    ● 네이버 기사를 크롤링 하여 얻은 자료이기에 네이버 뉴스의 카테고리 분류 방식과 같습니다.

    ● 네이버 크롤링은 <https://github.com/forkonlp/N2H4/> 의 도움을 얻었습니다.

    ● test결과 정확도는 76.7%입니다.



>SPEC
    
    ● python3에서 작동합니다.

    ● pickle,time, nltk,konlpy,requests,bs4 를 사용했습니다.

	
 
>지원기능
	
    ● url입력하면 그 url의 카테고리 추정

    ● 문장 입력하면 url의 카테고리 추정

  
How to Use
-------------

시작하기
-------------
    from get_sentence_and_test import Guess #모듈 import
	
    trained_classifier = Guess('naive_classifier3.pickle')
    
    #다운받은 pickle의 이름('naive_classifier 3.pickle')을 입력합니다.
  
object를 return합니다.
	
  
*주의* : 4get_sentence_and_test.py와 naive_classifier3.pickle을 현재 디렉토리(ex.C://Python35)에 저장해주세요.  
  
url로 카테고리 분석하기 
-------------
url의 본문 및 제목을 크롤링해 카테고리와 확률을 리턴합니다.

    category,probability = trained_classifier.by_url('https://wikidocs.net/16')
    
    #분석을 원하는 url을 입력하시면 됩니다.
		
>    return 값: str category(추정되는 카테고리)ex.'soc',   list probability(카테고리별 확률)ex.[(0.1,'soc'),(0.7,'eco')...]}
  
문장으로 카테고리 분석하기
-------------
문장을 읽고 카테고리와 확률을 리턴합니다.
    
    category,probability = trained_classifier.by_sentence('최고존엄 훼손...오바마 떠나기전 백악관 없어질 것')
    
		#분석을 원하는 문장을 입력하시면 됩니다.

>    return 값: str category(추정되는 카테고리)ex.'soc',	   list probability(카테고리별 확률)ex.[(0.1,'soc'),(0.7,'eco')...]}
