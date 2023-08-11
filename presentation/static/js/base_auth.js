    let bg = document.querySelector('.mouse-parallax-bg');
    window.addEventListener('mousemove', function(e) {
        let x = e.clientX / window.innerWidth;
        let y = e.clientY / window.innerHeight;
        bg.style.transform = 'translate(-' + x * 150 + 'px, -' + y * 150 + 'px)';
    });

    function update(chat_id, date_message) {

    }



    let div_main = document.getElementsByClassName('chats')[0]

    $.ajax({
      url: '/get_chats',
      method: 'post',
      dataType: 'json',
      success: function(json_data){
        console.log(json_data)
        json_data.chats.sort(
                function (a, b){
                  return new Date(b.time) - new Date(a.time)
                }
        )
        for (let i = 0; i < json_data.chats.length; i++){
          let div = add_element_chat(json_data.chats[i].chat_id, json_data.chats[i].time, json_data.chats[i].user_with, json_data.chats[i].from_who, json_data.chats[i].last_message, json_data.chats[i].checked, json_data.chats[i].user_with_id)
          div_main.appendChild(div)
        }
      }
    });



  function add_element_chat(chat_id, time, user_with, from_who, last_message, checked, user_with_id) {
    // 1 +
    let div_add = document.createElement("div")
    div_add.setAttribute("class", "collapse mt-3")
    div_add.id = "collapse" + chat_id
    // 2 +
    let div_card = document.createElement("div")
    div_card.setAttribute("class", "card")
    // 3 +
    let button_exit = document.createElement("button")
    button_exit.setAttribute("class", "btn-close")
    button_exit.setAttribute("type", "button")
    button_exit.setAttribute("data-mdb-toggle", "collapse")
    let href = "#collapse" + chat_id
    button_exit.setAttribute("href", href)
    button_exit.style = "padding: 10px"
    // 4
    let div_card_body = document.createElement("div")
    div_card_body.setAttribute("class", "card-body")
    div_card_body.setAttribute("data-mdb-perfect-scrollbar", "true")
    div_card_body.style = "position: relative; height: 400px; overflow: auto;"
    div_card_body.id = "div" + chat_id
    // 5
    // Элементы чата тут будут
    let date_message
    $.ajax({
              url: '/get_dialog',
              method: 'post',
              dataType: 'json',
              contentType: 'application/json',
              data: JSON.stringify({"chat_id": chat_id}),
              success: function (data) {
                date_message = data.messages[data.messages.length - 1].msg_date
                for (let i = 0; i < data.messages.length; i++) {
                  if (data.messages[i].msg_from === "Я: ") {
                    let div_element_d_flex = document.createElement("div")
                    div_element_d_flex.setAttribute("class", "d-flex flex-row justify-content-end mb-4 pt-1")
                    let div_element = document.createElement("div")
                    let flag = 0
                    for (let j = i; j < data.messages.length; j++) {
                      flag++
                      if (data.messages[j].msg_from === "Я: ") {
                        let p1 = document.createElement("p")
                        p1.setAttribute("class", "small p-2 me-3 mb-1 text-white rounded-3 bg-info")
                        p1.textContent = data.messages[j].msg_text
                        div_element.appendChild(p1)
                      } else {
                        i = i + flag - 2
                        break
                      }
                      if (j === data.messages.length - 1) {
                        i = data.messages.length
                        break
                      }
                    }
                    let image = document.createElement("img")
                    image.src = "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp"
                    image.alt = ""
                    image.style = "width: 45px; height: 100%;"
                    div_element_d_flex.appendChild(div_element)
                    div_element_d_flex.appendChild(image)
                    div_card_body.appendChild(div_element_d_flex)
                  } else {
                    let div_element_d_flex = document.createElement("div")
                    div_element_d_flex.setAttribute("class", "d-flex flex-row justify-content-start")
                    let image = document.createElement("img")
                    image.src = "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava5-bg.webp"
                    image.alt = ""
                    image.style = "width: 45px; height: 100%;"
                    let div_element = document.createElement("div")
                    let flag = 0
                    for (let j = i; j < data.messages.length; j++) {
                      flag++
                      if (data.messages[j].msg_from !== "Я: ") {
                        let p1 = document.createElement("p")
                        p1.setAttribute("class", "small p-2 ms-3 mb-1 rounded-3")
                        p1.style = "background-color: #f5f6f7;"
                        p1.textContent = data.messages[j].msg_text
                        div_element.appendChild(p1)
                      } else {
                        i = i + flag - 2
                        break
                      }
                      if (j === data.messages.length - 1) {
                        i = data.messages.length
                        break
                      }
                    }
                    div_element_d_flex.appendChild(image)
                    div_element_d_flex.appendChild(div_element)
                    div_card_body.appendChild(div_element_d_flex)

                  }
                }
              }
            }
    );


    // 6
    let div_container = document.createElement("div")
    div_container.setAttribute("class", "container")
    // 7
    let div_row = document.createElement("div")
    div_row.setAttribute("class", "row card-footer text-muted align-items-center")
    // 8
    let div_column1 = document.createElement("div")
    div_column1.setAttribute("class", "col-md-10")
    // 9
    let textarea = document.createElement("textarea")
    textarea.id = "textarea" + chat_id
    textarea.setAttribute("class", "shoutbox-name form-control form-control-lg")
    textarea.setAttribute("type", "text")
    textarea.setAttribute("placeholder", "Введите сообщение")
    // 10
    let div_column2 = document.createElement("div")
    div_column2.setAttribute("class", "col-md-1")
    div_column2.style = "padding: 0 0 0 10px"
    // 11
    let a1 = document.createElement("a")
    a1.setAttribute("class", "ms-1 text-muted")
    a1.setAttribute("href", "#!")
    // 12
    let i1 = document.createElement("i")
    i1.setAttribute("class", "fas fa-paperclip")
    // 13
    let div_column3 = document.createElement("div")
    div_column3.setAttribute("class", "col-md-1")
    // 14
    let a2 = document.createElement("a")
    a2.setAttribute("class", "ms-3 link-info")
    a2.setAttribute("href", "#!")
    a2.addEventListener("click", function () {
      var input = document.getElementById("textarea" + chat_id)
      if (input.value !== ""){
        $.ajax({
          url: '/send_message',
          method: 'post',
          dataType: 'html',
          contentType:'application/json',
          data: JSON.stringify({"msg_text": input.value, "msg_to": user_with_id}),
          success: function(data){
            input.value = ""
          }
        });
      }
    })
    setInterval(function () {
      $.ajax({
        url: '/get_dialog',
        method: 'post',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({"chat_id": chat_id}),
        success: function (data) {
          if(new Date(data.messages[data.messages.length - 1].msg_date) > new Date(date_message)){
              // Собеседник
              var div_card_element = document.getElementById("div" + chat_id)
              let div_element_d_flex = document.createElement("div")
              div_element_d_flex.setAttribute("class", "d-flex flex-row justify-content-end mb-4 pt-1")
              let div_element = document.createElement("div")
              let image = document.createElement("img")
              image.src = "https://mdbcdn.b-cdn.net/img/Photos/new-templates/bootstrap-chat/ava2-bg.webp"
              image.alt = ""
              image.style = "width: 45px; height: 100%;"
              let p1 = document.createElement("p")
              p1.setAttribute("class", "small p-2 me-3 mb-1 text-white rounded-3 bg-info")
              p1.textContent = data.messages[data.messages.length - 1].msg_text
              div_element.appendChild(p1)
              div_element_d_flex.appendChild(div_element)
              div_element_d_flex.appendChild(image)
              div_card_element.appendChild(div_element_d_flex)
              date_message = data.messages[data.messages.length - 1].msg_date
          }
        }
      })
      console.log(date_message)
    }, 500)
    // 15
    let i2 = document.createElement("i")
    i2.setAttribute("class", "fas fa-paper-plane")
    // Соединяем элементы
    a2.appendChild(i2)
    div_column3.appendChild(a2)
    a1.appendChild(i1)
    div_column2.appendChild(a1)
    div_column1.appendChild(textarea)
    div_row.appendChild(div_column1)
    div_row.appendChild(div_column2)
    div_row.appendChild(div_column3)
    div_container.appendChild(div_row)
    div_card.appendChild(button_exit)
    div_card.appendChild(div_card_body)
    div_card.appendChild(div_container)
    div_add.appendChild(div_card) // !
    // 16!
    let br = document.createElement("br")
    // 17
    let a = document.createElement("a")

    a.setAttribute("data-mdb-toggle", "collapse")
    a.setAttribute("href", href)
    a.setAttribute("role", "button")
    a.setAttribute("aria-expanded", "false")
    // 18
    let div_card_body2 = document.createElement("div")
    div_card_body2.setAttribute("class", "card-body")
    // 19
    let div_card_pos = document.createElement("div")
    div_card_pos.setAttribute("class", "position-relative position-relative-example")
    // 20
    let div_card_pos_1 = document.createElement("div")
    div_card_pos_1.setAttribute("class", "position-absolute top-0 end-0 text-muted")
    let time_correct = new Date(time)
    let today = new Intl.DateTimeFormat('ru', {weekday: 'long'}).format(time_correct);
    let seconds = ""
    if (time_correct.getSeconds() < 10){
      seconds = "0" + time_correct.getSeconds()
    }
    else{
      seconds = time_correct.getSeconds()
    }
    div_card_pos_1.textContent = today + " " + time_correct.getHours() + ":" + seconds
    div_card_pos_1.style = "font-size: 75%"
    // 21 Уведомление!
    let div_card_pos_2 = document.createElement("div")
    if (checked === true){
      a.setAttribute("class", "card elements opacity-75")
    }else{
      a.setAttribute("class", "card elements")
      div_card_pos_2.setAttribute("class", "position-absolute top-0 start-50 text-warning")
      div_card_pos_2.textContent = "Уведомление!"
      div_card_pos_2.style = "font-size: 75%"
    }
    // 22
    let div_container2 = document.createElement("div")
    div_container2.setAttribute("class", "container")
    // 23
    let div_row2 = document.createElement("div")
    div_row2.setAttribute("class", "row")
    // 24
    let div_col1 = document.createElement("div")
    div_col1.setAttribute("class", "col-md-2")
    div_col1.style = "padding: 10px 0 10px 0"
    // 25
    let img = document.createElement("img")
    img.setAttribute("src", "https://blog.getbootstrap.com/assets/img/2022/05/docs-home.png")
    img.setAttribute("alt", "")
    img.setAttribute("class", "rounded-circle")
    img.style = "width: 45px; height: 45px"
    // 26
    let div_col2 = document.createElement("div")
    div_col2.setAttribute("class", "col-md-10")
    div_col2.style = "padding: 10px 0 0 10px"
    // 27
    let p1 = document.createElement("p")
    p1.setAttribute("class", "fw-bold mb-1 lang text-muted")
    p1.textContent = user_with
    // 28
    let div_flex = document.createElement("div")
    div_flex.setAttribute("class", "d-flex")
    // 29
    let span = document.createElement("div")
    span.setAttribute("class", "text-muted lang fw-bold")
    span.style = "font-size: 75%"
    span.textContent = from_who + ":"
    // 30
    let p2 = document.createElement("p")
    p2.setAttribute("class", "lang text-muted text-truncate")
    p2.style = "font-size: 75%"
    p2.textContent = last_message
    // Соединяем
    div_col2.appendChild(p1)
    div_flex.appendChild(span)
    div_flex.appendChild(p2)
    div_col2.appendChild(div_flex)
    div_col1.appendChild(img)
    div_row2.appendChild(div_col1)
    div_row2.appendChild(div_col2)
    div_container2.appendChild(div_row2)
    div_card_pos.appendChild(div_card_pos_1)
    div_card_pos.appendChild(div_card_pos_2)
    div_card_body2.appendChild(div_card_pos)
    div_card_body2.appendChild(div_container2)
    a.appendChild(div_card_body2) // !
    let div_main = document.createElement("div")
    div_main.appendChild(div_add)
    div_main.appendChild(br)
    div_main.appendChild(a)
    return div_main
  }

    $('.shoutbox-name').emojioneArea({
      emojiPlaceholder: ":smile_cat:",
      searchPlaceholder: "Поиск",
      buttonTitle: "Эмодзи",
      searchPosition: "top",
      pickerPosition: "top"
    });

var arrLang = {
  'en': {
    'mainpage': 'Main page',
    'support': 'Support',
    'profile': 'Profile',
    'my_profile': 'My profile',
    'my_friends': 'My subscriptions',
    'my_subscriptions': 'My courses',
    'my_achievements': 'My achievements',
    'achievements': 'Achievements',
    'timetable': 'My timetable',
    'settings': 'Settings',
    'reviews': 'Reviews',
    'aboutus': 'About us',
    'exit': 'Logout',
    'areusure': 'Are you sure you want to log out?',
    'confirmexit': 'Confirm logout',
    'logout': 'Log out of your account',
    'flag': 'flag-united-kingdom',
    'your_chats': 'Your chats',
    'admin': 'ADMINISTRATOR',
    'subscribe': 'Subscribe',
    'unsubscribe': 'Unsubscribe',
    'give_admin': 'Grant administrator permissions',
    'remove_admin': 'Depose administrator permissions',
    'info': 'More information',
    'subscriptions': 'Subscriptions',
    'subscriptions_': 'subscriptions',
    'subscribers': 'subscribers',
    'participant_in': 'Participant in',
    'founded_by_request': 'Found on request:',

    'users_courses': 'User\'s courses',
    'create_course': 'Create course',
    'course_creation': 'Course creation',
    'enter_course_data': 'Enter course data:',
    'create': 'Create',

    'createform': 'Create form',
    'form': 'Form',

    'maininfo': 'Main information',
    'changeava': 'Change avatar',
    'anachievements': 'Achievements',
    'name': 'Name',
    'surname': 'Surname',
    'phonenumber': 'Phone number',
    'email': 'Email',
    'city': 'City:',
    'city_': 'City',
    'university': 'University',
    'specialization': 'Specialization',
    'group': 'Group',
    'save': 'Save',

    'devteam': 'Development team',
    'pavel': 'Pavel',
    'pavinfo': 'Backend and frontend developer',
    'online': 'Online',
    'ilya': 'Ilya',
    'ilyinfo': 'Frontend developer',
    'offline': 'Offline',
    'anton': 'Anton',
    'antinfo': 'Backend developer',
    'afk': 'AFK',
    'devinfo': 'Information about developer',

    'my_notes': 'My notes',
    'my_tasks': 'My tasks',
    'month': 'Month',

    "monday": "MO",
    "tuesday": "TU",
    "wednesday": "WE",
    "thursday": "TH",
    "friday": "FR",
    "saturday": "SA",
    "sunday": "SU",

    "course": "Course",
    "courses": "Courses",
    "course_rating": "Course rating:",
    "rate_first": "This course has not been rated yet, be the first!",
    "go_to_course": "Go to the course",
    "edit_course": "Edit course",
    "delete_course": "Delete course",
    "course_participants": "Course participants",
    "desc": "Description",
    "thanks_for_your_feedback": "Thanks for the feedback!",
    "how_do_you_like_this_course": "How do you like this course?",
    "give_us_feedback": "Leave your feedback:",
    "what_about_comment": "What about the comment?",
    "course_participants_feedback": "Feedback from course participants",
    "feedback_without_comment": "--- Review without comment ---",
    "show_all_feedback": "View all course reviews",
    "confirm_delete_course": "Confirmation of course deletion",
    "are_u_sure_delete_course": "Are you sure you want to delete the course",
    "delete": "Delete",

    "course_participants_of": "Participants of the course",
    "curator": "CURATOR",
    "give_curator": "Grant curator permissions",
    "remove_curator": "Depose curator permissions",

    "course_content": "Course content",
    "test": "Test",
    "article": "Article",
    "done": "Done",
    "checking": "On checking",
    "not_done": "Not done",
    "show_summary": "View progress summary",
    "test_desc": "Answer the questions and get a prize",
    "article_desc": "Read the article and eat a candy",

    "course_summary": "Course summary",
    "course_unit": "Course task",
    "tesk_type": "Type",
    "status": "Status",
    "mark": "Mark",
    "unit": "Unit",
    "result": "Result",

    "read_article": "The article was read",

    "show_tries": "Viewing tries",
    "leaders_table": "Leaderboard",
    "progress_graphic": "Progress graphic",
    "friends_progress": "Friends\' Progress",
    "last_tries": "The results of your previous tries",
    "try_number": "Try number",
    "condition": "Condition",
    "viewing": "Viewing",
    "time_spent": "Time spent on passing",
    "show_try": "View try",
    "best_mark": "Best mark:",
    "best_mark_": "Best mark",
    "place": "Place",
    "user": "User",
    "graphic_desc": "The graphic of the distribution of users according to the best mark",
    "friends_table_desc": "Leaderboard among friends you are subscribed to",
    "marking_method": "Assessment method: Teacher",
    "start_test": "Start test",

    "try_showing": "Viewing try",
    "information": "Information",
    "question": "Question",
    "score": "Score:",
    "not_marked": "Not marked",
    "the_same_answer": "users gave the same answer to this task",
    "curator_comment": "Curator\'s comment:",
    "your_result": "Your result:",
    "your_time_spent": "Time passed ",

    "passing_the_test": "Passing the test",
    "complete_test": "Complete the test",

    "course_reviews": "Reviews of the course",

    "course_editing": "Editing the course",
    "check": "Checking",
    "edit": "Edit",
    "task_creation": "Creating a task",
    "choose_task_type": "Select the type of task to be created:",
    "confirm_delete_unit": "Confirmation of deleting a unit",
    "confirm_delete_test": "Confirmation of deleting the test",
    "confirm_delete_article": "Confirmation of deleting the article",
    "are_u_sure_delete_unit": "Are you sure you want to delete the unit",
    "are_u_sure_delete_test": "Are you sure you want to delete the test",
    "are_u_sure_delete_article": "Are you sure you want to delete the article",
    "unit_creation": "Creating a unit",
    "enter_unit_name": "Enter the name of the unit:",
    "save_course": "Save course",

    "article_edit": "Article editing",
    "article_edit_of": "Editing of article",
    "enter_article": "Entering an article (in Markdown)",
    "article_text": "Article text",
    "article_preview": "Article preview",
    "save_article": "Save article",

    "article_constructor": "Article constructor",

    "test_checking": "Checking test",
    "tires_results": "Tires results",
    "check_try": "Check the try",

    "test_checking_user": "Checking the try of user",
    "add_comment": "Add comment",
    "result_": "Result:",
    "complete_checking": "Complete checking",

    "test_editor_of": "Editing of test",
    "test_editor": "Test editor",
    "solo": "Solo answer",
    "multiple": "Multiple answer",
    "free": "Free answer",
    "detailed_free": "Detailed free answer",
    "info_block": "Informational unit",
    "add_question": "Add question",
    "save_test": "Save test",
    "add_answer": "Add answer",
    "delete_answer": "Delete answer",

    "test_constructor": "Test constructor",

    "access_denied": "Access denied",
    "but_you_can_subscribe": "But you can get access to the materials of this course by subscribing to it",
  },
  'ru': {
    'mainpage': 'Главная',
    'support': 'Поддержка',
    'profile': 'Профиль',
    'my_profile': 'Мой профиль',
    'my_friends': 'Мои подписки',
    'my_subscriptions': 'Мои курсы',
    'my_achievements': 'Мои награды',
    'achievements': 'Достижения',
    'timetable': 'Мое расписание',
    'settings': 'Настройки',
    'reviews': 'Отзывы',
    'aboutus': 'О нас',
    'exit': 'Выйти',
    'areusure': 'Вы точно хотите выйти?',
    'confirmexit': 'Подтверждение выхода',
    'logout': 'Выход из учетной записи',
    'flag': 'flag-russia',
    'your_chats': 'Ваши диалоги',
    'admin': 'АДМИНИСТРАТОР',
    'subscribe': 'Подписаться',
    'unsubscribe': 'Отписаться',
    'give_admin': 'Выдать полномочия администратора',
    'remove_admin': 'Низложить полномочия администратора',
    'info': 'Подробнее',
    'subscriptions': 'Подписки',
    'subscriptions_': 'подписки',
    'subscribers': 'подписчиков',
    'participant_in': 'Участник в',
    'founded_by_request': 'Найдено по запросу:',

    'users_courses': 'Пользовательские курсы',
    'create_course': 'Создать курс',
    'course_creation': 'Создание курса',
    'enter_course_data': 'Введите данные курса:',
    'create': 'Создать',

    'createform': 'Создание формы',
    'form': 'Форма',

    'maininfo': 'Основная информация',
    'changeava': 'Сменить аватар',
    'anachievements': 'Достижения',
    'name': 'Имя',
    'surname': 'Фамилия',
    'phonenumber': 'Номер телефона',
    'email': 'Электронная почта',
    'city': 'Город:',
    'city_': 'Город',
    'university': 'Институт',
    'specialization': 'Специальность',
    'group': 'Учебная группа',
    'save': 'Сохранить',

    'devteam': 'Команда разработчиков',
    'pavel': 'Павел',
    'pavinfo': 'Бэкенд и Фронтенд разработчик',
    'online': 'На сайте',
    'ilya': 'Илья',
    'ilyinfo': 'Фронтэнд разработчик',
    'offline': 'Оффлайн',
    'anton': 'Антон',
    'antinfo': 'Бэкенд разработчик',
    'afk': 'Спит',
    'devinfo': 'Информация о разработчике',

    'my_notes': 'Мои заметки',
    'my_tasks': 'Мои задачи',
    'month': 'Месяц',

    "monday": "ПН",
    "tuesday": "ВТ",
    "wednesday": "СР",
    "thursday": "ЧТ",
    "friday": "ПТ",
    "saturday": "СБ",
    "sunday": "ВС",

    "course": "Курс",
    "courses": "Курсы",
    "course_rating": "Рейтинг курса:",
    "rate_first": "Данный курс пока не оценили, будьте первым!",
    "go_to_course": "Перейти на курс",
    "edit_course": "Редактировать курс",
    "delete_course": "Удалить курс",
    "course_participants": "Участники курса",
    "desc": "Описание",
    "thanks_for_your_feedback": "Спасибо за отзыв!",
    "how_do_you_like_this_course": "Как вам данный курс?",
    "give_us_feedback": "Оставьте свой отзыв:",
    "what_about_comment": "А как насчёт комментария?",
    "course_participants_feedback": "Отзывы участников курса",
    "feedback_without_comment": "--- Отзыв без комментария ---",
    "show_all_feedback": "Посмотреть все отзывы о курсе",
    "confirm_delete_course": "Подтверждение удаления курса",
    "are_u_sure_delete_course": "Вы точно хотите удалить курс",
    "delete": "Удалить",

    "course_participants_of": "Участники курса",
    "curator": "КУРАТОР",
    "give_curator": "Выдать полномочия куратора",
    "remove_curator": "Низложить полномочия куратора",

    "course_content": "Содержание курса",
    "test": "Тест",
    "article": "Статья",
    "done": "Выполнено",
    "checking": "На проверке",
    "not_done": "Не выполнено",
    "show_summary": "Посмотреть сводку о прогрессе",
    "test_desc": "Ответьте на вопросы и получите приз",
    "article_desc": "Прочтите статью и съешьте конфетку",

    "course_summary": "Сводка о курсе",
    "course_unit": "Элемент курса",
    "tesk_type": "Тип",
    "status": "Статус",
    "mark": "Оценка",
    "unit": "Раздел",
    "result": "Итог",

    "read_article": "Статья прочитана",

    "show_tries": "Просмотр попыток",
    "leaders_table": "Таблица лидеров",
    "progress_graphic": "График прогресса",
    "friends_progress": "Прогресс друзей",
    "last_tries": "Результаты ваших предыдущих попыток",
    "try_number": "Номер попытки",
    "condition": "Состояние",
    "viewing": "Просмотр",
    "time_spent": "Потрачено времени на прохождение",
    "show_try": "Посмотреть попытку",
    "best_mark": "Высшая оценка:",
    "best_mark_": "Высшая оценка",
    "place": "Место",
    "user": "Пользователь",
    "graphic_desc": "График распределения пользователей по высшей оценке",
    "friends_table_desc": "Таблица лидеров среди друзей, на кого вы подписаны",
    "marking_method": "Метод оценивания: Преподаватель",
    "start_test": "Начать тест",

    "try_showing": "Просмотр попытки",
    "information": "Информация",
    "question": "Вопрос",
    "score": "Баллы:",
    "not_marked": "Не оценено",
    "the_same_answer": "пользователей дали такой же ответ на данное задание",
    "curator_comment": "Комментарий куратора:",
    "your_result": "Ваш результат:",
    "your_time_spent": "Прошло времени ",

    "passing_the_test": "Прохождение теста",
    "complete_test": "Завершить тест",

    "course_reviews": "Отзывы о курсе",

    "course_editing": "Редактирование курса",
    "check": "Проверка",
    "edit": "Редактировать",
    "task_creation": "Создание задания",
    "choose_task_type": "Выберите тип создаваемого задания:",
    "confirm_delete_unit": "Подтверждение удаления раздела",
    "confirm_delete_test": "Подтверждение удаления теста",
    "confirm_delete_article": "Подтверждение удаления статьи",
    "are_u_sure_delete_unit": "Вы точно хотите удалить раздел",
    "are_u_sure_delete_test": "Вы точно хотите удалить тест",
    "are_u_sure_delete_article": "Вы точно хотите удалить статью",
    "unit_creation": "Создание раздела",
    "enter_unit_name": "Введите название раздела:",
    "save_course": "Сохранить курс",

    "article_edit": "Составление статьи",
    "enter_article": "Ввод статьи (в Markdown)",
    "article_text": "Текст статьи",
    "article_preview": "Превью вашей статьи",
    "save_article": "Сохранить статью",

    "article_constructor": "Конструктор статей",

    "test_checking": "Проверка теста",
    "tires_results": "Результаты попыток",
    "check_try": "Проверить попытку",

    "test_checking_user": "Проверка попытки пользователя",
    "add_comment": "Добавить комментарий",
    "result_": "Результат:",
    "complete_checking": "Завершить проверку",

    "test_editor_of": "Редактор теста",
    "test_editor": "Редактор теста",
    "solo": "Единственный ответ",
    "multiple": "Множественный ответ",
    "free": "Краткий свободный ответ",
    "detailed_free": "Свободный ответ",
    "info_block": "Информационный блок",
    "add_question": "Добавить вопрос",
    "save_test": "Сохранить тест",

    "test_constructor": "Конструктор тестов",

    "access_denied": "Доступ запрещён",
    "but_you_can_subscribe": "Но вы можете получить доступ к материалам данного курса, подписавшись на него",
  }
}

  $(function() {
    $('.translate').click(function() {
      var lang = $(this).attr('id');
      $('.lang').each(function(index, item) {
        $(this).text(arrLang[lang][$(this).attr('key')]);
		$('.curflag').removeClass('flag-united-kingdom').removeClass('flag-russia').addClass(arrLang[lang][$('.curflag').attr('key')]);
      });
	  let vis = document.getElementById("ru-tick").style.visibility;
		if (vis.valueOf() == "visible".valueOf()){
			document.getElementById("ru-tick").style.visibility = "hidden";
			document.getElementById("en-tick").style.visibility = "visible";
			localStorage.setItem('language', 'en')
		} else {
			document.getElementById("ru-tick").style.visibility = "visible";
			document.getElementById("en-tick").style.visibility = "hidden";
			localStorage.setItem('language', 'ru')
		}
    });
  });

  let lang = localStorage.getItem('language');
  if(lang.valueOf() == 'en'.valueOf()){
      document.getElementById("ru-tick").style.visibility = "hidden";
      document.getElementById("en-tick").style.visibility = "visible";
  } else {
      document.getElementById("ru-tick").style.visibility = "visible";
      document.getElementById("en-tick").style.visibility = "hidden";
  }
  $('.lang').each(function(index, item) {
      $(this).text(arrLang[lang][$(this).attr('key')]);
      $('.curflag').removeClass('flag-united-kingdom').removeClass('flag-russia').addClass(arrLang[lang][$('.curflag').attr('key')]);
  });