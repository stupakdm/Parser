import requests
import pandas as pd
import numpy as np
import re
import time

cities = '''					<section><p><b>Адыгея Республика</b></p><ul class="cities"><li><a href="/1/24/">Майкоп</a></li><li><a href="/1/372/">Яблоновский</a></li></ul></section><section><p><b>Алтай Республика</b></p><ul class="cities"><li><a href="/4/503/">Горно-Алтайск</a></li></ul></section><section><p><b>Алтайский край</b></p><ul class="cities"><li><a href="/22/106/">Барнаул</a></li><li><a href="/22/511/">Бийск</a></li><li><a href="/22/459/">Рубцовск</a></li></ul></section><section><p><b>Амурская область</b></p><ul class="cities"><li><a href="/28/516/">Благовещенск</a></li><li><a href="/28/322/">Свободный</a></li></ul></section><section><p><b>Архангельская область</b></p><ul class="cities"><li><a href="/29/1/">Архангельск</a></li><li><a href="/29/426/">Северодвинск</a></li></ul></section><section><p><b>Астраханская область</b></p><ul class="cities"><li><a href="/30/2/">Астрахань</a></li><li><a href="/30/275/">Ахтубинск</a></li><li><a href="/30/206/">Знаменск</a></li></ul></section><section><p><b>Башкортостан Республика</b></p><ul class="cities"><li><a href="/2/54/">Уфа</a></li><li><a href="/2/292/">Белорецк</a></li><li><a href="/2/509/">Бирск</a></li><li><a href="/2/299/">Ишимбай</a></li><li><a href="/2/294/">Кумертау</a></li><li><a href="/2/332/">Мелеуз</a></li><li><a href="/2/96/">Нефтекамск</a></li><li><a href="/2/73/">Сибай</a></li><li><a href="/2/97/">Стерлитамак</a></li></ul></section><section><p><b>Белгородская область</b></p><ul class="cities"><li><a href="/31/3/">Белгород</a></li><li><a href="/31/512/">Майский</a></li><li><a href="/31/437/">Старый Оскол</a></li></ul></section><section><p><b>Брянская область</b></p><ul class="cities"><li><a href="/32/4/">Брянск</a></li><li><a href="/32/2273/">Кокино</a></li><li><a href="/32/404/">Новозыбков</a></li><li><a href="/32/333/">Унеча</a></li></ul></section><section><p><b>Бурятия Республика</b></p><ul class="cities"><li><a href="/3/141/">Улан-Удэ</a></li></ul></section><section><p><b>Владимирская область</b></p><ul class="cities"><li><a href="/33/7/">Владимир</a></li><li><a href="/33/490/">Ковров</a></li><li><a href="/33/2249/">Мстера</a></li><li><a href="/33/94/">Муром</a></li><li><a href="/33/203/">Покров</a></li></ul></section><section><p><b>Волгоградская область</b></p><ul class="cities"><li><a href="/34/8/">Волгоград</a></li><li><a href="/34/416/">Волжский</a></li><li><a href="/34/430/">Камышин</a></li></ul></section><section><p><b>Вологодская область</b></p><ul class="cities"><li><a href="/35/9/">Вологда</a></li><li><a href="/35/136/">Череповец</a></li></ul></section><section><p><b>Воронежская область</b></p><ul class="cities"><li><a href="/36/10/">Воронеж</a></li><li><a href="/36/508/">Борисоглебск</a></li><li><a href="/36/364/">Россошь</a></li></ul></section><section><p><b>Дагестан Республика</b></p><ul class="cities"><li><a href="/5/25/">Махачкала</a></li><li><a href="/5/315/">Буйнакск</a></li><li><a href="/5/502/">Дербент</a></li><li><a href="/5/316/">Избербаш</a></li><li><a href="/5/317/">Каспийск</a></li><li><a href="/5/403/">Кизляр</a></li><li><a href="/5/425/">Хасавюрт</a></li><li><a href="/5/569/">Чиркей</a></li></ul></section><section><p><b>Еврейская АО</b></p><ul class="cities"><li><a href="/79/510/">Биробиджан</a></li></ul></section><section><p><b>Забайкальский край</b></p><ul class="cities"><li><a href="/75/60/">Чита</a></li></ul></section><section><p><b>Ивановская область</b></p><ul class="cities"><li><a href="/37/12/">Иваново</a></li><li><a href="/37/464/">Шуя</a></li></ul></section><section><p><b>Ингушетия Республика</b></p><ul class="cities"><li><a href="/6/2283/">Магас</a></li><li><a href="/6/494/">Назрань</a></li></ul></section><section><p><b>Иркутская область</b></p><ul class="cities"><li><a href="/38/13/">Иркутск</a></li><li><a href="/38/515/">Ангарск</a></li><li><a href="/38/507/">Братск</a></li><li><a href="/38/348/">Усть-Илимск</a></li></ul></section><section><p><b>Кабардино-Балкария</b></p><ul class="cities"><li><a href="/7/29/">Нальчик</a></li></ul></section><section><p><b>Калининградская область</b></p><ul class="cities"><li><a href="/39/15/">Калининград</a></li><li><a href="/39/442/">Полесск</a></li></ul></section><section><p><b>Калмыкия Республика</b></p><ul class="cities"><li><a href="/8/61/">Элиста</a></li></ul></section><section><p><b>Калужская область</b></p><ul class="cities"><li><a href="/40/16/">Калуга</a></li><li><a href="/40/138/">Обнинск</a></li></ul></section><section><p><b>Камчатский край</b></p><ul class="cities"><li><a href="/41/38/">Петропавловск-Камчатский</a></li></ul></section><section><p><b>Карачаево-Черкессия</b></p><ul class="cities"><li><a href="/9/59/">Черкесск</a></li><li><a href="/9/492/">Карачаевск</a></li></ul></section><section><p><b>Карелия Республика</b></p><ul class="cities"><li><a href="/10/491/">Петрозаводск</a></li></ul></section><section><p><b>Кемеровская область</b></p><ul class="cities"><li><a href="/42/17/">Кемерово</a></li><li><a href="/42/440/">Белово</a></li><li><a href="/42/408/">Междуреченск</a></li><li><a href="/42/92/">Новокузнецк</a></li><li><a href="/42/99/">Прокопьевск</a></li><li><a href="/42/434/">Юрга</a></li></ul></section><section><p><b>Кировская область</b></p><ul class="cities"><li><a href="/43/18/">Киров</a></li></ul></section><section><p><b>Коми Республика</b></p><ul class="cities"><li><a href="/11/489/">Сыктывкар</a></li><li><a href="/11/462/">Воркута</a></li><li><a href="/11/347/">Усинск</a></li><li><a href="/11/468/">Ухта</a></li></ul></section><section><p><b>Костромская область</b></p><ul class="cities"><li><a href="/44/19/">Кострома</a></li><li><a href="/44/1501/">Караваево</a></li></ul></section><section><p><b>Краснодарский край</b></p><ul class="cities"><li><a href="/23/20/">Краснодар</a></li><li><a href="/23/446/">Анапа</a></li><li><a href="/23/513/">Армавир</a></li><li><a href="/23/340/">Белореченск</a></li><li><a href="/23/505/">Геленджик</a></li><li><a href="/23/103/">Ейск</a></li><li><a href="/23/107/">Новороссийск</a></li><li><a href="/23/185/">Славянск-на-Кубани</a></li><li><a href="/23/47/">Сочи</a></li><li><a href="/23/1292/">Темрюк</a></li><li><a href="/23/273/">Тихорецк</a></li><li><a href="/23/401/">Туапсе</a></li></ul></section><section><p><b>Красноярский край</b></p><ul class="cities"><li><a href="/24/21/">Красноярск</a></li><li><a href="/24/432/">Ачинск</a></li><li><a href="/24/463/">Лесосибирск</a></li><li><a href="/24/115/">Норильск</a></li></ul></section><section><p><b>Крым Республика</b></p><ul class="cities"><li><a href="/84/535/">Севастополь</a></li><li><a href="/84/2242/">Армянск</a></li><li><a href="/84/2240/">Евпатория</a></li><li><a href="/84/2426/">Керчь</a></li><li><a href="/84/632/">Симферополь</a></li><li><a href="/84/2284/">Совхозное</a></li><li><a href="/84/2241/">Ялта</a></li></ul></section><section><p><b>Курганская область</b></p><ul class="cities"><li><a href="/45/486/">Курган</a></li><li><a href="/45/2269/">Курган-16</a></li><li><a href="/45/487/">Лесниково</a></li><li><a href="/45/465/">Шадринск</a></li></ul></section><section><p><b>Курская область</b></p><ul class="cities"><li><a href="/46/22/">Курск</a></li></ul></section><section><p><b>Ленинградская область</b></p><ul class="cities"><li><a href="/47/312/">Волхов</a></li><li><a href="/47/343/">Выборг</a></li><li><a href="/47/298/">Гатчина</a></li><li><a href="/47/255/">Ивангород</a></li><li><a href="/47/485/">Луга</a></li><li><a href="/47/2282/">Мурино</a></li><li><a href="/47/449/">Сосновый Бор</a></li></ul></section><section><p><b>Липецкая область</b></p><ul class="cities"><li><a href="/48/23/">Липецк</a></li><li><a href="/48/499/">Елец</a></li></ul></section><section><p><b>Магаданская область</b></p><ul class="cities"><li><a href="/49/135/">Магадан</a></li></ul></section><section><p><b>Марий Эл Республика</b></p><ul class="cities"><li><a href="/12/483/">Йошкар-Ола</a></li></ul></section><section><p><b>Мордовия Республика</b></p><ul class="cities"><li><a href="/13/481/">Саранск</a></li><li><a href="/13/361/">Рузаевка</a></li></ul></section><section><p><b>Московская область</b></p><ul class="cities"><li><a href="/50/74/">Балашиха</a></li><li><a href="/50/1808/">Большие Вязёмы</a></li><li><a href="/50/82/">Бронницы</a></li><li><a href="/50/147/">Видное</a></li><li><a href="/50/102/">Волоколамск</a></li><li><a href="/50/116/">Воскресенск</a></li><li><a href="/50/261/">Голицыно</a></li><li><a href="/50/87/">Дмитров</a></li><li><a href="/50/117/">Домодедово</a></li><li><a href="/50/111/">Дубна</a></li><li><a href="/50/85/">Егорьевск</a></li><li><a href="/50/84/">Жуковский</a></li><li><a href="/50/127/">Клин</a></li><li><a href="/50/75/">Коломна</a></li><li><a href="/50/122/">Королев</a></li><li><a href="/50/1064/">Котельники</a></li><li><a href="/50/2275/">Красково</a></li><li><a href="/50/69/">Красногорск</a></li><li><a href="/50/110/">Люберцы</a></li><li><a href="/50/2271/">Малаховка</a></li><li><a href="/50/88/">Мытищи</a></li><li><a href="/50/113/">Одинцово</a></li><li><a href="/50/124/">Орехово-Зуево</a></li><li><a href="/50/79/">Павловский Посад</a></li><li><a href="/50/195/">Протвино</a></li><li><a href="/50/67/">Пущино</a></li><li><a href="/50/351/">Рыбное</a></li><li><a href="/50/125/">Сергиев Посад</a></li><li><a href="/50/80/">Серпухов</a></li><li><a href="/50/2239/">Сколково</a></li><li><a href="/50/1897/">Старотеряево</a></li><li><a href="/50/68/">Ступино</a></li><li><a href="/50/112/">Фрязино</a></li><li><a href="/50/83/">Химки</a></li><li><a href="/50/2270/">Черкизово</a></li><li><a href="/50/540/">Электроизолятор</a></li><li><a href="/50/91/">Электросталь</a></li></ul></section><section><p><b>Мурманская область</b></p><ul class="cities"><li><a href="/51/28/">Мурманск</a></li><li><a href="/51/396/">Апатиты</a></li></ul></section><section><p><b>Нижегородская область</b></p><ul class="cities"><li><a href="/52/30/">Нижний Новгород</a></li><li><a href="/52/514/">Арзамас</a></li><li><a href="/52/193/">Выкса</a></li><li><a href="/52/460/">Дзержинск</a></li><li><a href="/52/184/">Княгинино</a></li><li><a href="/52/194/">Павлово</a></li><li><a href="/52/363/">Саров</a></li></ul></section><section><p><b>Новгородская область</b></p><ul class="cities"><li><a href="/53/480/">Великий Новгород</a></li></ul></section><section><p><b>Новосибирская область</b></p><ul class="cities"><li><a href="/54/32/">Новосибирск</a></li><li><a href="/54/443/">Куйбышев</a></li></ul></section><section><p><b>Омская область</b></p><ul class="cities"><li><a href="/55/33/">Омск</a></li><li><a href="/55/439/">Тара</a></li></ul></section><section><p><b>Оренбургская область</b></p><ul class="cities"><li><a href="/56/35/">Оренбург</a></li><li><a href="/56/410/">Бузулук</a></li><li><a href="/56/256/">Новотроицк</a></li><li><a href="/56/433/">Орск</a></li></ul></section><section><p><b>Орловская область</b></p><ul class="cities"><li><a href="/57/34/">Орел</a></li><li><a href="/57/376/">Ливны</a></li></ul></section><section><p><b>Пензенская область</b></p><ul class="cities"><li><a href="/58/36/">Пенза</a></li><li><a href="/58/2263/">Пенза-5</a></li></ul></section><section><p><b>Пермский край</b></p><ul class="cities"><li><a href="/59/37/">Пермь</a></li><li><a href="/59/436/">Березники</a></li><li><a href="/59/276/">Лысьва</a></li><li><a href="/59/474/">Соликамск</a></li><li><a href="/59/466/">Чайковский</a></li></ul></section><section><p><b>Приморский край</b></p><ul class="cities"><li><a href="/25/5/">Владивосток</a></li><li><a href="/25/454/">Арсеньев</a></li><li><a href="/25/448/">Большой Камень</a></li><li><a href="/25/496/">Находка</a></li><li><a href="/25/477/">Уссурийск</a></li></ul></section><section><p><b>Псковская область</b></p><ul class="cities"><li><a href="/60/39/">Псков</a></li><li><a href="/60/506/">Великие Луки</a></li></ul></section><section><p><b>Ростовская область</b></p><ul class="cities"><li><a href="/61/40/">Ростов-на-Дону</a></li><li><a href="/61/444/">Волгодонск</a></li><li><a href="/61/207/">Гуково</a></li><li><a href="/61/518/">Зерноград</a></li><li><a href="/61/139/">Каменск-Шахтинский</a></li><li><a href="/61/246/">Миллерово</a></li><li><a href="/61/479/">Новочеркасск</a></li><li><a href="/61/501/">Персиановский</a></li><li><a href="/61/473/">Таганрог</a></li><li><a href="/61/142/">Шахты</a></li></ul></section><section><p><b>Рязанская область</b></p><ul class="cities"><li><a href="/62/41/">Рязань</a></li></ul></section><section><p><b>Самарская область</b></p><ul class="cities"><li><a href="/63/43/">Самара</a></li><li><a href="/63/475/">Кинель</a></li><li><a href="/63/452/">Сызрань</a></li><li><a href="/63/93/">Тольятти</a></li></ul></section><section><p><b>Саратовская область</b></p><ul class="cities"><li><a href="/64/45/">Саратов</a></li><li><a href="/64/131/">Балаково</a></li><li><a href="/64/132/">Балашов</a></li><li><a href="/64/183/">Вольск</a></li><li><a href="/64/461/">Энгельс</a></li></ul></section><section><p><b>Саха (Якутия) Республика</b></p><ul class="cities"><li><a href="/14/63/">Якутск</a></li><li><a href="/14/457/">Мирный</a></li><li><a href="/14/458/">Нерюнгри</a></li><li><a href="/14/324/">Октемцы</a></li><li><a href="/14/1495/">Чурапча</a></li></ul></section><section><p><b>Сахалинская область</b></p><ul class="cities"><li><a href="/65/62/">Южно-Сахалинск</a></li></ul></section><section><p><b>Свердловская область</b></p><ul class="cities"><li><a href="/66/11/">Екатеринбург</a></li><li><a href="/66/909/">Верхняя Пышма</a></li><li><a href="/66/228/">Верхняя Салда</a></li><li><a href="/66/229/">Краснотурьинск</a></li><li><a href="/66/238/">Лесной</a></li><li><a href="/66/89/">Нижний Тагил</a></li><li><a href="/66/302/">Новоуральск</a></li></ul></section><section><p><b>Северная Осетия Алания</b></p><ul class="cities"><li><a href="/15/6/">Владикавказ</a></li></ul></section><section><p><b>Смоленская область</b></p><ul class="cities"><li><a href="/67/46/">Смоленск</a></li><li><a href="/67/373/">Вязьма</a></li></ul></section><section><p><b>Ставропольский край</b></p><ul class="cities"><li><a href="/26/27/">Ставрополь</a></li><li><a href="/26/498/">Ессентуки</a></li><li><a href="/26/137/">Кисловодск</a></li><li><a href="/26/120/">Лермонтов</a></li><li><a href="/26/402/">Минеральные Воды</a></li><li><a href="/26/413/">Невинномысск</a></li><li><a href="/26/495/">Пятигорск</a></li></ul></section><section><p><b>Тамбовская область</b></p><ul class="cities"><li><a href="/68/48/">Тамбов</a></li><li><a href="/68/482/">Мичуринск</a></li></ul></section><section><p><b>Татарстан Республика</b></p><ul class="cities"><li><a href="/16/14/">Казань</a></li><li><a href="/16/517/">Альметьевск</a></li><li><a href="/16/286/">Бугульма</a></li><li><a href="/16/500/">Елабуга</a></li><li><a href="/16/186/">Лениногорск</a></li><li><a href="/16/72/">Набережные Челны</a></li><li><a href="/16/417/">Нижнекамск</a></li></ul></section><section><p><b>Тверская область</b></p><ul class="cities"><li><a href="/69/49/">Тверь</a></li><li><a href="/69/2265/">Тверь-22</a></li></ul></section><section><p><b>Томская область</b></p><ul class="cities"><li><a href="/70/50/">Томск</a></li><li><a href="/70/441/">Северск</a></li></ul></section><section><p><b>Тульская область</b></p><ul class="cities"><li><a href="/71/51/">Тула</a></li><li><a href="/71/114/">Новомосковск</a></li></ul></section><section><p><b>Тыва Республика</b></p><ul class="cities"><li><a href="/17/471/">Кызыл</a></li></ul></section><section><p><b>Тюменская область</b></p><ul class="cities"><li><a href="/72/52/">Тюмень</a></li><li><a href="/72/493/">Ишим</a></li><li><a href="/72/472/">Тобольск</a></li></ul></section><section><p><b>Удмуртская Республика</b></p><ul class="cities"><li><a href="/18/65/">Ижевск</a></li><li><a href="/18/358/">Воткинск</a></li><li><a href="/18/504/">Глазов</a></li><li><a href="/18/359/">Сарапул</a></li></ul></section><section><p><b>Ульяновская область</b></p><ul class="cities"><li><a href="/73/53/">Ульяновск</a></li><li><a href="/73/453/">Димитровград</a></li></ul></section><section><p><b>Хабаровский край</b></p><ul class="cities"><li><a href="/27/55/">Хабаровск</a></li><li><a href="/27/488/">Комсомольск-на-Амуре</a></li></ul></section><section><p><b>Хакасия Республика</b></p><ul class="cities"><li><a href="/19/467/">Абакан</a></li><li><a href="/19/306/">Саяногорск</a></li></ul></section><section><p><b>Ханты-Мансийский AO</b></p><ul class="cities"><li><a href="/81/56/">Ханты-Мансийск</a></li><li><a href="/81/105/">Нижневартовск</a></li><li><a href="/81/101/">Сургут</a></li></ul></section><section><p><b>Челябинская область</b></p><ul class="cities"><li><a href="/74/58/">Челябинск</a></li><li><a href="/74/429/">Златоуст</a></li><li><a href="/74/484/">Магнитогорск</a></li><li><a href="/74/394/">Миасс</a></li><li><a href="/74/313/">Миасское</a></li><li><a href="/74/287/">Озерск</a></li><li><a href="/74/415/">Снежинск</a></li><li><a href="/74/234/">Трехгорный</a></li><li><a href="/74/469/">Троицк</a></li></ul></section><section><p><b>Чеченская Республика</b></p><ul class="cities"><li><a href="/20/66/">Грозный</a></li></ul></section><section><p><b>Чувашская Республика</b></p><ul class="cities"><li><a href="/21/57/">Чебоксары</a></li><li><a href="/21/423/">Алатырь</a></li></ul></section><section><p><b>Чукотский AO</b></p><ul class="cities"><li><a href="/82/236/">Анадырь</a></li></ul></section><section><p><b>Ярославская область</b></p><ul class="cities"><li><a href="/76/64/">Ярославль</a></li><li><a href="/76/476/">Рыбинск</a></li><li><a href="/76/328/">Тутаев</a></li></ul></section>
'''
#test = np.array([['a', 'a', 'a', 'a', 'a', 'a', 'a']])

#itemprop="url"><a href="http://noungi.ru" 
#itemprop="email">ngi_04@mail.ru</p>
#itemprop="telephone"><a href="tel:+74965738839">+7 (496) 573-88-39 </a></div>

#<meta name="Keywords" content="РГСУ в г. Клин, Российский государственный социальный университет — филиал в г. Клин, общая информация,
url = 'https://vuz.edunetwork.ru'

def get_info(text):
  info = ['-']*7
  end = '<p class="bold"'
  #end2 = 
  title = '<meta name="Keywords" content='
  start_info ='<h2>Общая информация</h2>'
  fl = 0

  find_full_name = '"legalName">(.*?)</p>'
  country = 'addressCountry'

  for i in range(len(text)):
    if title in text[i]:
      a = re.findall(r'<meta name="Keywords" content="(.*?), общая информация', text[i])
      a = a[0].split(', ')
      info[0] = a[1].strip()
      info[2] = a[0].strip()
    #if start_info in text[i]:
    try:
      if 'legalName' in text[i]:
        fl = 1
        a = re.findall(r'"legalName">(.*?)</p>', text[i])
        info[1] = a[0].strip()
      
      if 'addressCountry' in text[i] and fl == 1:
        info[3] = text[i+1].strip()
      
      if 'itemprop="url"' in text[i] and fl == 1:
        a = re.findall(r'itemprop="url"><a href="(.*?)" target="_blank">', text[i])
        info[4] = a[0].strip()
      
      if 'itemprop="email"' in text[i] and fl == 1:
        a = re.findall(r'itemprop="email">(.*?)</p>', text[i])
        info[5] = a[0].strip()

      if 'itemprop="telephone"' in text[i] and fl == 1:
        a = re.findall(r'itemprop="telephone"><a href="tel:(.*?)">', text[i])
        info[6] = a[0].strip()
    except IndexError:
      continue
    if end in text[i]:
      break
  print(info[0])
  return info


def parse_universe(text):
  unit = 'unit-name'
  end = '<span id="helper-title">В вузы, отмеченные' 
  links = []
  for i in range(len(text)):
    if end in text[i]:
      break
    if unit in text[i]:
      link = re.findall(r'<a href="(.*?)"', text[i+1])
      links.append(link)
  return links

def get_text_url(k , url_text):
  test = np.array([['a', 'a', 'a', 'a', 'a', 'a', 'a']])
  page = '/?page='
  for i in range(0, k):
    time.sleep(np.random.randint(2,8))
    full_url = url+url_text+page+str(i)
    res = ses.get(full_url)
    #time.sleep(np.random.randint(2,8))
    text = res.text.split('\n')
    links = parse_universe(text)
    for link in links:
      time.sleep(np.random.randint(2,8))
      res = ses.get(url+link[0])
      text = res.text.split('\n')
      info = np.array([get_info(text)])
      test = np.append(test, info, axis=0)
  return test[1:test.shape[0]]

#df = pd.DataFrame(columns = ('Название ВУЗа', 'Полное название ВУЗА', 'Сокращенное название ВУЗА', 'Адрес', 'Сайт', 'Почта', 'Телефон'))
if __name__ == '__main__':
  test = np.array([['a', 'a', 'a', 'a', 'a', 'a', 'a']])
  #url = 'https://vuz.edunetwork.ru'
  moscow_url = '/77/'
  spb_url = '/78/'
  page = '/?page='
  unit = 'unit-name'
  end = '<span id="helper-title">В вузы, отмеченные'
  all_links = re.findall(r'<a href="(.*?)/"', cities)
  with requests.Session() as ses:
      #ses.headers = {'HH-User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:91.0) Gecko/20100101 Firefox/91.0'}
      ses.headers = {'HH-User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 YaBrowser/22.1.0.2510 Yowser/2.5 Safari/537.36"}
      
      test = np.append(test, get_text_url(5, moscow_url), axis = 0)
      test = test[1:test.shape[0]]
      test = np.append(test, get_text_url(3, spb_url), axis= 0)

      for link in all_links:
        test = np.append(test, get_text_url(1, link), axis=0)

      df = pd.DataFrame(test, columns = ['Название', 'Полное название', 'Сокращенное название', 'Адрес', 'Сайт', 'Почта', 'Телефон'])
      df.to_csv('Вся информация по университетам России.csv', index = False, encoding = 'utf-8')
      #print(test)
      #res = ses.get(url)
      #text = res.text.split('\n')
      ses.close()
