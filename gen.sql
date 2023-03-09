

/* USERS GENERATION */
CREATE TABLE usernames
(
    id serial PRIMARY KEY,
    username text
);

WITH list AS (
    SELECT ARRAY['yuakaltal', 'Vilonyugsd', 'Vaotnaus', 'Laerovkhi', 'Chelibkyul', 'Lokabenrd', 'Taetonen', 'Myaesloshz', 'Paledpogay', 'Zesopn', 'Maedliveh', 'Panilkait', 'Saasagzors', 'Savasilenh', 'Vialnischi', 'Vaokle', 'Laelsn', 'Kaokag', 'Saovilmas', 'Leapagiy', 'Senakbeyuv', 'Pevyupmeil', 'Kousozzhuf', 'Megokanchm', 'Nerashodos', 'Nogavnavs', 'Tinoor', 'Rakokavit', 'Ziiveh', 'Vaalchovkm', 'Nanagaraes', 'Taavyubale', 'Geasnano', 'Zepak', 'Chodaryu', 'Schay', 'Biaens', 'Kelan', 'Saasla', 'Senomal', 'Lemikaub', 'Vevazont', 'Vaanzhal', 'Teachtah', 'Schetyun', 'Zuabn', 'Lanip', 'Lakines', 'Seezhakn', 'Keeti', 'Kevosava', 'Bamienh', 'Doosior', 'Ryuuvumf', 'Baaum', 'Nepaun', 'Vyulyuke', 'Feeva', 'Lounayun', 'Seape', 'Leirbaum', 'Nenetvup', 'Dadanol', 'Vaaktens', 'Liin', 'Donaern', 'Kaokkne', 'Shos', 'Valimva', 'Namaanv', 'Kuss', 'Saovvha', 'Lealsh', 'Meat', 'Loilum', 'Nopr', 'Shem', 'Meak', 'Kaevmit', 'Baschad', 'Rabaal', 'Zeloosf', 'Maarda', 'Keneif', 'Neomm', 'Bapn', 'Lityuor', 'Def', 'Vell', 'Kuokyun', 'Leaal', 'Vizh', 'Neisden', 'Taarpas', 'Neotdya', 'Zibovd', 'sibaspa', 'gaalei', 'rakota', 'kepka']
      AS words
    )
INSERT INTO usernames (username)
  SELECT unnest(words)
    FROM list;


CREATE TABLE emails
(
  id serial PRIMARY KEY,
  email text
);

WITH list AS (
    SELECT ARRAY['cgreuter@att.net', 'danneng@hotmail.com', 'rasca@icloud.com', 'staikos@comcast.net', 'tarreau@optonline.net', 'cremonini@mac.com', 'matloff@aol.com', 'barnett@optonline.net', 'matty@outlook.com', 'pakaste@att.net', 'errxn@sbcglobal.net', 'monkeydo@optonline.net', 'burniske@me.com', 'frosal@att.net', 'jimmichie@aol.com', 'jusdisgi@gmail.com', 'dvdotnet@hotmail.com', 'engelen@yahoo.com', 'eminence@yahoo.com', 'skippy@hotmail.com', 'galbra@mac.com', 'facet@hotmail.com', 'mcrawfor@outlook.com', 'monopole@verizon.net', 'doche@msn.com', 'isorashi@msn.com', 'zilla@comcast.net', 'kdawson@yahoo.ca', 'themer@me.com', 'granboul@yahoo.com', 'cliffski@yahoo.ca', 'adamk@yahoo.com', 'sfoskett@live.com', 'fraser@msn.com', 'russotto@verizon.net', 'sinkou@aol.com', 'tbeck@yahoo.com', 'raides@live.com', 'syncnine@aol.com', 'seasweb@me.com', 'giafly@me.com', 'shazow@yahoo.ca', 'tmccarth@verizon.net', 'jimmichie@sbcglobal.net', 'mcmillan@mac.com', 'brbarret@optonline.net', 'dowdy@yahoo.com', 'campbell@yahoo.com', 'hyper@gmail.com', 'keutzer@yahoo.com', 'bartak@aol.com', 'chronos@icloud.com', 'ardagna@icloud.com', 'daveed@aol.com', 'gslondon@aol.com', 'rafasgj@sbcglobal.net', 'dsowsy@verizon.net', 'rsteiner@comcast.net', 'keutzer@me.com', 'rjones@verizon.net', 'ateniese@gmail.com', 'aardo@optonline.net', 'maradine@me.com', 'warrior@comcast.net', 'harryh@hotmail.com', 'dbindel@mac.com', 'falcao@gmail.com', 'chrisk@comcast.net', 'kobayasi@yahoo.com', 'nelson@mac.com', 'jbarta@live.com', 'citadel@sbcglobal.net', 'jaxweb@msn.com', 'gboss@comcast.net', 'ngedmond@yahoo.com', 'reeds@mac.com', 'madler@yahoo.ca', 'nimaclea@sbcglobal.net', 'aardo@sbcglobal.net', 'kimvette@msn.com', 'kspiteri@hotmail.com', 'rhavyn@optonline.net', 'pizza@me.com', 'jmgomez@sbcglobal.net', 'kannan@msn.com', 'research@me.com', 'jesse@att.net', 'akoblin@aol.com', 'noneme@yahoo.ca', 'sthomas@gmail.com', 'tristan@optonline.net', 'mcast@optonline.net', 'rattenbt@msn.com', 'plover@optonline.net', 'chlim@verizon.net', 'drewf@yahoo.ca', 'odlyzko@comcast.net', 'multiplx@me.com', 'psharpe@msn.com', 'conteb@att.net']
      AS words
    )
INSERT INTO emails (email)
  SELECT unnest(words)
    FROM list;


CREATE TABLE cities
(
    id serial PRIMARY KEY,
    city text
);

WITH list AS (
    SELECT ARRAY['Irkutsk', 'Moscow', 'Irkutsk', 'Achinsk', 'Saint Petersburg', 'Krasnoyarsk', 'Krasnoyarsk', 'Abakan', 'Abakan', 'Achinsk', 'Abakan', 'Achinsk', 'Irkutsk', 'Achinsk', 'Achinsk', 'Achinsk', 'Abakan', 'Saint Petersburg', 'Moscow', 'Achinsk', 'Achinsk', 'Irkutsk', 'Irkutsk', 'Saint Petersburg', 'Krasnoyarsk', 'Moscow', 'Moscow', 'Saint Petersburg', 'Achinsk', 'Abakan', 'Krasnoyarsk', 'Abakan', 'Krasnoyarsk', 'Krasnoyarsk', 'Achinsk', 'Moscow', 'Abakan', 'Krasnoyarsk', 'Irkutsk', 'Abakan', 'Irkutsk', 'Moscow', 'Achinsk', 'Achinsk', 'Saint Petersburg', 'Abakan', 'Moscow', 'Achinsk', 'Irkutsk', 'Abakan', 'Moscow', 'Achinsk', 'Irkutsk', 'Krasnoyarsk', 'Irkutsk', 'Krasnoyarsk', 'Abakan', 'Abakan', 'Achinsk', 'Moscow', 'Irkutsk', 'Achinsk', 'Irkutsk', 'Krasnoyarsk', 'Irkutsk', 'Irkutsk', 'Krasnoyarsk', 'Saint Petersburg', 'Achinsk', 'Achinsk', 'Achinsk', 'Abakan', 'Saint Petersburg', 'Abakan', 'Moscow', 'Saint Petersburg', 'Krasnoyarsk', 'Achinsk', 'Saint Petersburg', 'Irkutsk', 'Irkutsk', 'Irkutsk', 'Moscow', 'Krasnoyarsk', 'Krasnoyarsk', 'Abakan', 'Krasnoyarsk', 'Krasnoyarsk', 'Moscow', 'Abakan', 'Saint Petersburg', 'Krasnoyarsk', 'Saint Petersburg', 'Achinsk', 'Abakan', 'Krasnoyarsk', 'Moscow', 'Moscow', 'Saint Petersburg', 'Krasnoyarsk']
      AS words
    )
INSERT INTO cities (city)
  SELECT unnest(words)
    FROM list;

CREATE TABLE passwords
(
    id serial PRIMARY KEY,
    password text
);

WITH list AS (
    SELECT ARRAY['jw2MQy_Q', 'LKh8q8*$', 'K-5Gxm]K', 'vN.&8%K?', 'uJ{FMN3{', 'm>T9up/C', 'xE]zzdF2', 'C7?%)rUs', 'j[3_WEpX', 'pV6&7N[L', 'nm}472Db', '7&eJMs)*', 'vw&T6FH{', 'QEn*P8A)', '6$b{?A=!', 'K{kC2kyJ', '*6%DY^}k', '-r3q9DZH', '}^>qnSu8', 'S=b23/A!', '4Xx!t=/W', 't%eWn8]?', '-FKu+7Ca', '*n5Yjz6v', '7FkJxt+Q', 'U6_8cu-E', 'zJh3!hfc', '$2fh7Lw)', 'S3g^FnJH', 'bNfFy6.5', 'A]^/y6v^', '2Hy{ETj^', 'j(8[ebT=', '8!8g-W=>', 'E2Xd?jXy', '@d)Vj8KZ', 'r]2mUNL&', '}Yf94MxC', 'P/k4BB&$', 'q3)ayzQY', '%sE7ppn9', '!VZpZp2A', '7B)wM]5t', 'Yvq=6{Cc', 'Z@P4QSWh', '^z9+B86P', 'bHW@p]9Q', 'fE.)c69A', '^L%xk3?8', '5X5b[@-?', '?6MVCzh/', 'KwJ=F=!3', 'cN/e/5LF', '7E]uDDD}', 'm-8UE2yg', '9Khaq-kZ', 'hZ?Dez9N', 't-Z[Q_Z9', 'wQWBy7q-', '}6ea5X6v', '*q/5WtJ]', '.G_uG5XK', 'qeC=Gn2m', '>w9++6Lf', 'pN^tF5Tv', 'x@&8^TN.', '}?%&e>X2', '9[gh(3qJ', 'b7[y&dsA', '[QrM2UYf', '8P*}X^Py', 'PY@&e2$p', '=XSmCp9Z', 'k7cm/A{-', 'z8)eEjtF', 'e?})[>L4', '}mSv7^V^', '+K@N7h=[', '2mC[W/Lt', '6$Xh@957', '9GEzcy)a', '+cL[G4$-', 'bg8X5k*p', ']9eU%nvV', '@9LQUfbk', 'gZh3_St{', 'ZU!5Z6$w', 'C.[5f2UU', '*d}Z3=?T', '=%ufrRp8', '>cL5n.wA', 'h2m-mSU=', 'q+FA3A2&', 'aFH>9[km', '+R5c9_h4', 'R9h!d(@N', 'gDU24gA%', 'r($)vEX6', '2Hq$.T[$', 'K?7u&JxJ']
      AS words
    )
INSERT INTO passwords (password)
  SELECT unnest(words)
    FROM list;

WITH random_rows AS(
SELECT u.username, e.email, c.city, p.password
FROM usernames u, emails e, cities c, passwords p
WHERE u.id = e.id AND e.id = c.id AND c.id = p.id
)
INSERT INTO users(username, email, city, password)
	SELECT username, email, city, password
	FROM random_rows;

WITH list AS (
    SELECT ARRAY['логика', 'математика', 'информатика', 'теория принятия решений', 'статистика', 'Общественные науки', 'антропология', 'история', 'социология', 'право', 'политология', 'культурология', 'экономика', 'Военная наука', 'Гуманитарные науки', 'лингвистика', 'психология', 'литературоведение', 'искусствоведение', 'педагогика', 'этика', 'эстетика', 'журналистика', 'филология', 'Естественные (эмпирические) науки', 'антропология', 'астрономия', 'биология', 'ветеринария', 'география', 'геология', 'медицина', 'метеорология', 'океанология', 'физика', 'химия', 'Технические науки', 'архитектура', 'биотехнология', 'информатика', 'кибернетика', 'кораблестроение', 'космонавтика', 'материаловедение', 'механика', 'системотехника', 'строительство', 'химическая технология', 'электротехника', 'энергетика', 'обработка древесины', 'Алгоритмы и алгоритмические языки', 'Архитектура ЭВМ и язык ассемблера', 'Практикум на ЭВМ', 'Дискретная математика', 'Система программирования', 'Операционные системы', 'Учебная производственная практика (Практикум на ЭВМ)', 'Базы данных', 'Суперкомпьютер и параллельная обработка данных', 'Компьютерная графика', 'Физические основы построения ЭВМ', '«Методы оптимизации»', 'Основы кибернетики', 'Введение в сети ЭВМ', 'Основы программной инженерии', 'Дисциплина по выбору «Формальные языки и автоматы»', 'Дисциплина по выбору «Сложность алгоритмов»', '«Компьютерное моделирование динамических систем»', 'Сети ЭВМ и безопасность', 'Искусственный интеллект', 'Математические методы параллельных и распределенных вычислений', 'Алгоритмы и структуры данных', 'Иностранный язык', 'Математика', 'Математическая логика и теория алгоритмов', 'Объектно-ориентированное программирование', 'Операционные системы', 'Отладка программного обеспечения (факультатив)', 'Прикладная теория графов', 'Программирование на языке С++ (факультатив)', 'Русский язык и культура речи', 'Схемотехника', 'Физика', 'Физическая культура', 'Философия', 'Численные методы в АСО и У', 'Электротехника и электроника', 'Психология и педагогика', 'Системное программное обеспечение', 'Системный анализ', 'Теория автоматов', 'Теория вычислительных систем', 'Теория принятия решений', 'Управление данными', 'Физическая культура', 'Финансовый менеджмент', 'ЭВМ и периферийные устройства', 'Администрирование сетевых информационных систем', 'Информационный менеджмент']
      AS words
    )
INSERT INTO courses (name)
  SELECT unnest(words)
    FROM list;


WITH list AS (
    SELECT ARRAY['Travel the World', 'Learn to Surf', 'See the Northern Lights', 'Take a Road Trip', 'Learn to Play the Guitar', 'Write a Novel', 'Dye Your Hair Pink', 'Go Hang Gliding', 'Get a Tattoo', 'Buy a House', 'Ride a Camel Through the Desert', 'Let go of a Floating Lantern', 'Go to the top of the Eiffel Tower', 'Marry the Love of Your Life', 'Take a Photo a Day for a Year', 'Go Whale Watching', 'Go Skiing', 'Run a Marathon', 'Go Stargazing', 'Get Your Dream Job', 'Paint a Picture', 'Ride on a Hot Air Balloon', 'Bake a Cake', 'Practice Yoga', 'Cliff Jump', 'Reach Your Goal Weight', 'Ride a Horse on the Beach', 'Visit a Vineyard', 'Start a Family', 'Visit Hawaii', 'Adopt a Cat', 'Go Camping with Friends', 'Have a Tea Party', 'Walk on the Great Wall of China', 'Make Every Recipe in a Cookbook', 'Have a Water Balloon Fight', 'Visit All Seven Continents', 'Have a Picnic', 'Go on a Safari', 'Catch a Fish', 'Brew Your Own Beer', 'Soak in Iceland’s Blue Lagoon', 'Read a Book a Month', 'Ride a Motorcycle', 'Visit Machu Picchu', 'Learn to Make Sushi', 'Ride a Roller Coaster', 'Hike a Volcano', 'Graduate College', 'Visit a Spa', 'Volunteer with Elephants', 'Host a Cocktail Party', 'Start a Garden', 'Visit all 50 States', 'Adopt a Dog', 'Become Fluent in Spanish', 'Redecorate Your Home', 'Attend a Beach Bonfire', 'See the Pyramids in Egypt', 'Be and Extra in a Movie', 'Go White Water Rafting', 'Fly First Class', 'Solve a Rubik’s Cube', 'Go Skinny Dipping', 'Learn to Swing Dance', 'Live in New York City', 'Make Pasta from Scratch', 'Have a Movie Marathon', 'Watch the Sun Set', 'Have a Pillow Fight', 'Learn to Knit', 'Visit the Taj Mahal', 'Go Apple Picking', 'Stand Under a Waterfall', 'Get a Professional Manicure', 'Dance in the Rain', 'See Your Favorite Band in Concert', 'Stand Under the Hollywood Sign', 'Find a Four Leaf Clover', 'Hike the Appalachian Trail', 'Start a Blog', 'Ride on a Ferris Wheel', 'Get a Book Signed by Your Favorite Author', 'Walk Across the Golden Gate Bridge', 'Eat Paella in Spain', 'Learn to Drive Stick Shift', 'Visit Santorini in Greece', 'Learn How to Tie a Tie', 'Take a Pottery Class', 'See the Statue of Liberty', 'Learn to Skateboard', 'Visit the Amazon', 'Go Indoor Rock Climbing', 'Be Served Breakfast in Bed', 'Travel to Bali', 'Ride on a Gondola', 'Take an Alaskan Cruise', 'Go Scuba Diving', 'Live in Europe', 'Fall in Love']
      AS words
    )
INSERT INTO tasks (name, user_id, date)
  SELECT unnest(words), floor(random() * 99 + 1), CURRENT_DATE
    FROM list;

WITH list AS (
    SELECT ARRAY['determined', 'immense', 'nasty', 'colossal', 'grubby', 'large', 'abrupt', 'exuberant', 'glorious', 'troubled', 'diminutive', 'intrigued', 'panicky', 'costly', 'hungry', 'lovely', 'disturbed', 'foolish', 'perplexed', 'adventurous', 'funny', 'happy', 'wicked', 'condescending', 'grumpy', 'lazy', 'despicable', 'ideal', 'narrow', 'aloof', 'greasy', 'helpless', 'zippy', 'cooperative', 'dappy', 'lonely', 'courageous', 'hurt', 'lucky', 'agitated', 'gaudy', 'healthy', 'zany', 'exasperated', 'friendly', 'tender', 'confused', 'handsome', 'livid', 'brave', 'gritty', 'hollow', 'dizzy', 'fresh', 'teeny', 'distressed', 'irate', 'perfect', 'corny', 'top', 'loose', 'exhilarated', 'frothy', 'terrible', 'excited', 'frightened', 'tense', 'acidic', 'supa', 'gorgeous', 'unsightly', 'bored', 'grieving', 'high', 'aggressive', 'fuzzy', 'harebrained', 'yummy', 'alert', 'graceful', 'helpful', 'zealous', 'adorable', 'frustrating', 'haya', 'upset', 'bright', 'grotesque', 'homely', 'cruel', 'icy', 'mysterious', 'extensive', 'topich', 'tricky', 'frantic', 'quizzical', 'dilapidated', 'impressionable', 'outrageous']
      AS words
    )
INSERT INTO achievements (name, course_id)
  SELECT 'THE MOST ' || unnest(words), floor(random() * 99 + 1)
    FROM list;

INSERT INTO curators (user_id, course_id)
    SELECT floor(random() * 99 + 1), floor(random() * 99 + 1)
    FROM generate_series(1, 100);

INSERT INTO courses_rel (user_id, course_id)
    SELECT floor(random() * 99 + 1), floor(random() * 99 + 1)
    FROM generate_series(1, 100);

INSERT INTO achieve_rel (ach_id, user_id)
    SELECT floor(random() * 99 + 1), floor(random() * 99 + 1)
    FROM generate_series(1, 100);

WITH list AS (
    SELECT ARRAY['determined', 'immense', 'nasty', 'colossal', 'grubby', 'large', 'abrupt', 'exuberant', 'glorious', 'troubled', 'diminutive', 'intrigued', 'panicky', 'costly', 'hungry', 'lovely', 'disturbed', 'foolish', 'perplexed', 'adventurous', 'funny', 'happy', 'wicked', 'condescending', 'grumpy', 'lazy', 'despicable', 'ideal', 'narrow', 'aloof', 'greasy', 'helpless', 'zippy', 'cooperative', 'dappy', 'lonely', 'courageous', 'hurt', 'lucky', 'agitated', 'gaudy', 'healthy', 'zany', 'exasperated', 'friendly', 'tender', 'confused', 'handsome', 'livid', 'brave', 'gritty', 'hollow', 'dizzy', 'fresh', 'teeny', 'distressed', 'irate', 'perfect', 'corny', 'top', 'loose', 'exhilarated', 'frothy', 'terrible', 'excited', 'frightened', 'tense', 'acidic', 'supa', 'gorgeous', 'unsightly', 'bored', 'grieving', 'high', 'aggressive', 'fuzzy', 'harebrained', 'yummy', 'alert', 'graceful', 'helpful', 'zealous', 'adorable', 'frustrating', 'haya', 'upset', 'bright', 'grotesque', 'homely', 'cruel', 'icy', 'mysterious', 'extensive', 'topich', 'tricky', 'frantic', 'quizzical', 'dilapidated', 'impressionable', 'outrageous']
      AS words
    )
INSERT INTO reviews (text, user_id, course_id, rate)
  SELECT 'MY RATE -  COURSE IS ' || unnest(words), floor(random() * 99 + 1),
         floor(random() * 99 + 1), floor(random() * 9 + 1)
    FROM list;

DROP TABLE usernames;
DROP TABLE emails;
DROP TABLE cities;
DROP TABLE passwords;