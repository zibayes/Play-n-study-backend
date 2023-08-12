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
    "unit_result": "Result of unit",

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

    "new_note": "New note",
    "name_": "Name:",
    "note_": "Note:",
    "exit": "Exit",
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
    "unit_result": "Итог раздела",

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

    "new_note": "Новая заметка",
    "name_": "Название:",
    "note_": "Заметка:",
  },
  'de': {
    'mainpage': 'Startseite',
    'support': 'support',
    'profile': 'Profil',
    'my_profile': 'Mein Profil',
    'my_friends': 'Meine Abonnements',
    'my_subscriptions': 'Meine Kurse',
    'my_achievements': 'Meine Belohnungen',
    'achievements': 'Erfolge',
    'timetable': 'Mein Zeitplan',
    'settings': 'Einstellungen',
    'reviews': 'Bewertungen',
    'aboutus': 'Über uns',
    'exit': 'Beenden',
    'areusure': 'Möchten Sie unbedingt aussteigen?',
    'confirmexit': 'Abmeldung bestätigen',
    'logout': 'Abmelden von Ihrem Konto',
    'flag': 'flag-germany',
    'your_chats': 'Ihre Dialoge',
    'admin': 'administrator',
    'subscribe': 'Abonnieren',
    'unsubscribe': 'Abbestellen',
    'give_admin': 'Administratorberechtigungen erteilen',
    'remove_admin': 'Administratorrechte ablegen',
    'info': 'Weitere Informationen',
    'subscriptions': 'Abonnements',
    'subscriptions_': 'Abonnements',
    'subscribers': 'Abonnenten',
    'participant_in': 'Teilnehmer in',
    'founded_by_request': 'Auf Anfrage gefunden:',

    'users_courses': 'Benutzerdefinierte Kurse',
    'create_course': 'Kurs erstellen',
    'course_creation': 'Kurs erstellen',
    'enter_course_data': 'Kursdaten eingeben:',
    'create': 'Erstellen',

    'createform': 'Formular erstellen',
    'form': 'Form',

    'maininfo': 'Grundlegende Informationen',
    'changeava': 'Avatar ändern',
    'anachievements': 'Erfolge',
    'name': 'Name',
    'surname': 'Nachname',
    'phonenumber': 'Telefonnummer',
    'email': 'E-Mail',
    'city': 'Stadt:',
    'city_': 'Stadt',
    'university': 'Institut',
    'specialization': 'Spezialität',
    'group': 'Lerngruppe',
    'save': 'Speichern',

    'devteam': 'Entwicklerteam',
    'pavel': 'Paul',
    'pavinfo': 'Backend und Frontend Entwickler',
    'online': 'Online',
    'ilya': 'ilya',
    'ilyinfo': 'Frontend-Entwickler',
    'offline': 'Offline',
    'anton': 'Anton',
    'antinfo': 'Backend-Entwickler',
    'afk': 'Schläft',
    'devinfo': 'Entwicklerinformationen',

    'my_notes': 'Meine Notizen',
    'my_tasks': 'Meine Aufgaben',
    'month': 'Monat',

    "monday": "MO",
    "tuesday": "W",
    "wednesday": "MI",
    "thursday": "DO",
    "friday": "FR",
    "saturday": "SA",
    "sunday": "SUN",

    "course": "Kurs",
    "courses": "Kurse",
    "course_rating": "Kursbewertung:",
    "rate_first": "Dieser Kurs wurde noch nicht bewertet, sei der erste!",
    "go_to_course": "Kurs wechseln",
    "edit_course": "Kurs bearbeiten",
    "delete_course": "Kurs löschen",
    "course_participants": "Kursteilnehmer",
    "desc": "Beschreibung",
    "thanks_for_your_feedback": "Vielen Dank für Ihr Feedback!",
    "how_do_you_like_this_course": "Wie gefällt Ihnen dieser Kurs?",
    "give_us_feedback": "Hinterlassen Sie Ihr Feedback:",
    "what_about_comment": "Was ist mit einem Kommentar?",
    "course_participants_feedback": "Feedback der Kursteilnehmer",
    "feedback_without_comment": "--- Feedback ohne Kommentar ---",
    "show_all_feedback": "Alle Erfahrungsberichte anzeigen",
    "confirm_delete_course": "Bestätigung, dass der Kurs gelöscht wird",
    "are_u_sure_delete_course": "Sie möchten den Kurs unbedingt löschen",
    "delete": "Löschen",

    "course_participants_of": "Kursteilnehmer",
    "curator": "KURATOR",
    "give_curator": "Berechtigung zum Kurator erteilen",
    "remove_curator": "Die Autorität des Kurators aufheben",

    "course_content": "Kursinhalte",
    "test": "Test",
    "article": "Artikel",
    "done": "Fertig",
    "checking": "Im Check",
    "not_done": "fehlgeschlagen",
    "show_summary": "Fortschrittsbericht anzeigen",
    "test_desc": "Beantworte die Fragen und erhalte einen Preis",
    "article_desc": "Lesen Sie den Artikel und essen Sie Süßigkeiten",

    "course_summary": "Kursübersicht",
    "course_unit": "Kurselement",
    "tesk_type": "Typ",
    "status": "Status",
    "mark": "Bewertung",
    "unit": "Partition",
    "result": "Ergebnis",
    "unit_result": "Partitionszusammenfassung",

    "read_article": "Artikel wurde gelesen",

    "show_tries": "Versuche anzeigen",
    "leaders_table": "Bestenliste",
    "progress_graphic": "Fortschrittsplan",
    "friends_progress": "Fortschritt von Freunden",
    "last_tries": "Ergebnisse Ihrer vorherigen Versuche",
    "try_number": "Versuchsnummer",
    "condition": "Zustand",
    "viewing": "Anzeigen",
    "time_spent": "Zeitaufwand für das Durchlaufen",
    "show_try": "Versuch ansehen",
    "best_mark": "Höchste Bewertung:",
    "best_mark_": "Höchste Bewertung",
    "place": "Place",
    "user": "Benutzer",
    "graphic_desc": "Zeitplan für die Verteilung der Benutzer nach höchster Bewertung",
    "friends_table_desc": "Die Bestenliste unter den Freunden, denen du abonniert hast",
    "marking_method": "Bewertungsmethode: Lehrer",
    "start_test": "Test starten",

    "try_showing": "Einen Versuch anzeigen",
    "information": "Information",
    "question": "Frage",
    "score": "Punkte:",
    "not_marked": "Nicht bewertet",
    "the_same_answer": "Benutzer haben dieselbe Antwort auf diese Aufgabe gegeben",
    "curator_comment": "Kommentar des Kurators:",
    "your_result": "Ihr Ergebnis ist:",
    "your_time_spent": "Die Zeit ist vergangen ",

    "passing_the_test": "Test bestehen",
    "complete_test": "Test abschließen",

    "course_reviews": "Kursbewertungen",

    "course_editing": "Kurs bearbeiten",
    "check": "Überprüfen",
    "edit": "Bearbeiten",
    "task_creation": "Auftrag erstellen",
    "choose_task_type": "Wählen Sie den Typ des zu erstellenden Auftrags aus:",
    "confirm_delete_unit": "Bestätigung des Löschens einer Partition",
    "confirm_delete_test": "Bestätigung, dass der Test gelöscht wurde",
    "confirm_delete_article": "Bestätigung des Löschens eines Artikels",
    "are_u_sure_delete_unit": "Sie möchten die Partition unbedingt löschen",
    "are_u_sure_delete_test": "Sie möchten den Test unbedingt löschen",
    "are_u_sure_delete_article": "Sie möchten den Artikel unbedingt löschen",
    "unit_creation": "Partition erstellen",
    "enter_unit_name": "Geben Sie einen Namen für die Partition ein:",
    "save_course": "Kurs speichern",

    "article_edit": "Artikel erstellen",
    "enter_article": "Artikel eingeben (in Markdown)",
    "article_text": "Artikeltext",
    "article_preview": "Vorschau Ihres Artikels",
    "save_article": "Artikel speichern",

    "article_constructor": "Artikel-Designer",

    "test_checking": "Test prüfen",
    "tires_results": "Ergebnisse der Versuche",
    "check_try": "Versuch prüfen",

    "test_checking_user": "Benutzerversuch prüfen",
    "add_comment": "Kommentar hinzufügen",
    "result_": "Ergebnis:",
    "complete_checking": "Prüfung abschließen",

    "test_editor_of": "Testeditor",
    "test_editor": "Testeditor",
    "solo": "Die einzige Antwort",
    "multiple": "Multiple Antwort",
    "free": "Kurze freie Antwort",
    "detailed_free": "Freie Antwort",
    "info_block": "Informationsblock",
    "add_question": "Frage hinzufügen",
    "save_test": "Test speichern",

    "test_constructor": "Testkonstruktor",

    "access_denied": "Zugriff verweigert",
    "but_you_can_subscribe": "Sie können jedoch auf den Inhalt dieses Kurses zugreifen, indem Sie ihn abonnieren",

    "new_note": "Neue Notiz",
    "name_": "Name:",
    "note_": "Hinweis:",
    },
    'fr': {
      'mainpage': 'Accueil',
      'support': 'Support',
      'profile': 'Profil',
      'my_profile': 'mon profil',
      'my_friends': 'mes abonnements',
      'my_subscriptions': 'mes cours',
      'my_achievements': 'mes récompenses',
      'achievements': 'Réalisations',
      'timetable': 'mon horaire',
      'settings': 'Paramètres',
      'reviews': 'Avis',
      'aboutus': 'À propos de nous',
      'exit': 'Quitter',
      'areusure': 'voulez-vous vraiment sortir?',
      'confirmexit': 'confirmation de sortie',
      'logout': 'Déconnexion du compte',
      'flag': 'flag-france',
      'your_chats': 'vos dialogues',
      'admin': 'ADMINISTRATEUR',
      'subscribe': 's\'Abonner',
      'unsubscribe': 'se Désabonner',
      'give_admin': 'Accorder des privilèges d\'administrateur',
      'remove_admin': 'Supprimer les privilèges d\'administrateur',
      'info': 'lire la Suite',
      'subscriptions': 'Abonnements',
      'subscriptions_': 'abonnements',
      'subscribers': 'abonnés',
      'participant_in': 'Participant à',
      'founded_by_request': 'trouvé sur demande:',

      'users_courses': 'cours Personnalisés',
      'create_course': 'Créer un cours',
      'course_creation': 'Création d\'un cours',
      'enter_course_data': 'Entrez les données du cours:',
      'create': 'Créer',

      'createform': 'Créer un formulaire',
      'form': 'Forme',

      'maininfo': 'informations de Base',
      'changeava': 'Changer d\'avatar',
      'anachievements': 'Réalisations',
      'name': 'Nom',
      'surname':'nom de Famille',
      'phonenumber': 'Numéro de téléphone',
      'email': 'Email',
      'city': 'Ville:',
      'city_': 'Ville',
      'university': 'Institut',
      'specialization': 'Spécialité',
      'group': 'groupe d\'Étude',
      'save': 'Enregistrer',

      'devteam': 'équipe de développement',
      'pavel': 'Paul',
      'pavinfo': 'backend and Frontend Developer',
      'online': 'en ligne',
      'ilya': 'Ilya',
      'ilyinfo': 'Frontend Developer',
      'offline': 'Offline',
      'anton': 'Anton',
      'antinfo': 'développeur Backend',
      'afk': 'Dort',
      'devinfo': 'informations sur le développeur',

      'my_notes': 'mes notes',
      'my_tasks': 'mes tâches',
      'month': 'Mois',

      "monday": "LUN",
      "tuesday": "W",
      "wednesday": "CF",
      "thursday": "JEUDI",
      "friday": "VEN",
      "saturday": "SAT",
      "sunday": "Sun",

      "course": "Cours",
      "courses": "Cours",
      "course_rating": "Classement du cours:",
      "rate_first": "ce cours n'a pas encore été évalué, soyez le premier!",
      "go_to_course": "Aller au cours",
      "edit_course":"Modifier le cours",
      "delete_course": "Supprimer le cours",
      "course_participants": "Participants au cours",
      "desc": "Description",
      "thanks_for_your_feedback": "Merci pour vos commentaires!",
      "how_do_you_like_this_course": "comment Aimez-vous ce cours?",
      "give_us_feedback": "Donnez votre avis:",
      "what_about_comment": "qu'en est-il du commentaire?",
      "course_participants_feedback": "Commentaires des participants au cours",
      "feedback_without_comment": "- - - Commentaire sans commentaire - - -",
      "show_all_feedback": "Voir tous les commentaires sur le cours",
      "confirm_delete_course": "Confirmation de la suppression du cours",
      "are_u_sure_delete_course":"vous voulez vraiment supprimer le cours",
      "delete": "Supprimer",

      "course_participants_of": "Participants au cours",
      "curator": "CURATOR",
      "give_curator":"Donner l'autorité du conservateur",
      "remove_curator":"Supprimer l'autorité du conservateur",

      "course_content": "Contenu du cours",
      "test": "Test",
      "article": "Article",
      "done": "Terminé",
      "checking": "en cours de vérification",
      "not_done": "échec",
      "show_summary":"Voir le résumé des progrès",
      "test_desc":"Répondez aux questions et obtenez le prix",
      "article_desc": "Lisez l'article et mangez des bonbons",

      "course_summary":"Résumé du cours",
      "course_unit": "élément de cours",
      "tesk_type": "Type",
      "status": "Status",
      "mark": "Score",
      "unit": "Partition",
      "result": "Total",
      "unit_result":"Total de la section",

      "read_article": "Article lu",

      "show_tries": "Afficher les tentatives",
      "leaders_table": "classement",
      "progress_graphic":"Graphique de progression",
      "friends_progress": "Progression des amis",
      "last_tries": "Résultats de vos tentatives précédentes",
      "try_number": "numéro de tentative",
      "condition": "Condition",
      "viewing": "Viewing",
      "time_spent":"temps Passé à passer",
      "show_try": "Voir la tentative",
      "best_mark": "meilleur score:",
      "best_mark_":"meilleur score",
      "place": "Place",
      "user": "Utilisateur",
      "graphic_desc": "Graphique de la répartition des utilisateurs selon l'évaluation la plus élevée",
      "friends_table_desc": "classement des amis auxquels vous êtes abonné",
      "marking_method":"méthode d'évaluation: Enseignant",
      "start_test": "Commencer le test",

      "try_showing":"Afficher la tentative",
      "information": "Information",
      "question": "Question",
      "score": "Scores:",
      "not_marked": "Non évalué",
      "the_same_answer": "les utilisateurs ont donné la même réponse à cette tâche",
      "curator_comment": "Commentaire du conservateur:",
      "your_result": "votre résultat:",
      "your_time_spent": "le temps s'est Écoulé",

      "passing_the_test": "Passer le test",
      "complete_test": "Terminer le test",

      "course_reviews":"Avis sur le cours",

      "course_editing": "Modification du cours",
      "check": "Check",
      "edit": "Modifier",
      "task_creation": "Création d'une tâche",
      "choose_task_type": "Choisissez le type de travail à créer:",
      "confirm_delete_unit": "Confirmation de la suppression de la partition",
      "confirm_delete_test": "Confirmation de la suppression du test",
      "confirm_delete_article": "Confirmation de la suppression de l'article",
      "are_u_sure_delete_unit":"vous voulez vraiment supprimer la partition",
      "are_u_sure_delete_test": "voulez-vous vraiment supprimer le test",
      "are_u_sure_delete_article": "vous voulez vraiment supprimer l'article",
      "unit_creation": "Créer une partition",
      "enter_unit_name": "Entrez le nom de la section:",
      "save_course": "Enregistrer le cours",

      "article_edit": "Rédaction de l'article",
      "enter_article": "Entrée de l'article (dans Markdown)",
      "article_text":"Texte de l'article",
      "article_preview":"Aperçu de votre article",
      "save_article": "Enregistrer l'article",

      "article_constructor":"Constructeur d'articles",

      "test_checking":"Vérification du test",
      "tires_results": "résultats des tentatives",
      "check_try": "Vérifier la tentative",

      "test_checking_user":"Vérification de la tentative de l'utilisateur",
      "add_comment": "Ajouter un commentaire",
      "result_": "Résultat:",
      "complete_checking": "Terminer la vérification",

      "test_editor_of": "Éditeur de test",
      "test_editor":"Éditeur de test",
      "solo": "seule réponse",
      "multiple": "réponse Multiple",
      "free":"réponse Courte et gratuite",
      "detailed_free": "réponse Libre",
      "info_block": "bloc d'Informations",
      "add_question": "Ajouter une question",
      "save_test": "Enregistrer le test",

      "test_constructor":"Constructeur de test",

      "access_denied":"Accès refusé",
      "but_you_can_subscribe":"Mais vous pouvez accéder au contenu de ce cours en vous inscrivant",

      "new_note":"nouvelle Note",
      "name_": "Titre:",
      "note_":"Note:",
    },
    'es': {
      'mainpage':'Inicio',
      'support':'Support',
      'profile':'Perfil',
      'my_profile': 'mi perfil',
      'my_friends' :' mis suscripciones',
      'my_subscriptions' :' mis cursos',
      'my_achievements' :' mis recompensas',
      'achievements': 'Logros',
      'timetable': 'mi horario',
      'settings': 'Ajustes',
      'reviews': 'Reviews',
      'aboutus': 'Sobre nosotros',
      'exit': 'Salir',
      'areusure': '¿seguro que quieres salir?',
      'confirmexit' :' confirmación de salida',
      'logout': 'Cerrar sesión',
      'flag': 'flag-spain',
      'your_chats': 'Tus diálogos',
      'admin':'ADMIN',
      'subscribe':'Suscribirse',
      'unsubscribe':'darse de Baja',
      'give_admin': 'Otorgar privilegios de administrador',
      'remove_admin': 'Deponer privilegios de administrador',
      'info': 'Más información',
      'subscriptions': 'Suscripciones',
      'subscriptions_': 'suscripciones',
      'subscribers': 'suscriptores',
      'participant_in': 'Participante en',
      'founded_by_request': 'Encontrado para:',

      'users_courses': 'cursos Personalizados',
      'create_course': 'Crear curso',
      'course_creation': 'Crear un curso',
      'enter_course_data': 'Introduzca los datos del curso:',
      'create': 'Crear',

      'createform': 'Crear un formulario',
      'form': 'Forma',

      'maininfo': 'información Básica',
      'changeava': 'Cambiar avatar',
      'anachievements': 'Logros',
      'name':'Nombre',
      'surname':'Apellido',
      'phonenumber': 'número de Teléfono',
      'email':'email',
      'city':'Ciudad:',
      'city_':'Ciudad',
      'university':'Instituto',
      'specialization':'Especialidad',
      'group': 'grupo de Estudio',
      'save': 'Guardar',

      'devteam' :' equipo de desarrollo',
      'pavel':'Pablo',
      'pavinfo':'desarrollador de backend y Frontend',
      'online': 'En línea',
      'ilya':'Ilya',
      'ilyinfo': 'desarrollador Frontend',
      'offline': 'Offline',
      'anton': 'Anton',
      'antinfo': 'desarrollador de Backend',
      'afk':'Durmiendo',
      'devinfo': 'Información del desarrollador',

      'my_notes' :' mis notas',
      'my_tasks' :' mis tareas',
      'month': 'Mes',

      "monday": "LUNES",
      "tuesday":"MARTES",
      "wednesday": "MIÉ",
      "thursday": "JUE",
      "friday":"VIERNES",
      "saturday": "SAT",
      "sunday":"SUN",

      "course":"Curso",
      "courses": "Cursos",
      "course_rating": "Clasificación del curso:",
      "rate_first": "este curso aún no ha sido evaluado, ¡sea el primero!",
      "go_to_course": "Ir al curso",
      "edit_course": "Editar curso",
      "delete_course": "Eliminar curso",
      "course_participants": "Participantes del curso",
      "desc":"Descripción",
      "thanks_for_your_feedback": "¡Gracias por tus comentarios!",
      "how_do_you_like_this_course": "¿qué te Parece este curso?",
      "give_us_feedback": "Deja un comentario:",
      "what_about_comment": "¿qué tal un comentario?",
      "course_participants_feedback": "Opiniones de los participantes del curso",
      "feedback_without_comment": "- - - Opinión sin comentarios - - -",
      "show_all_feedback": "Ver todas las reseñas del curso",
      "confirm_delete_course": "confirmación de la eliminación del curso",
      "are_u_sure_delete_course": "seguro que quieres eliminar el curso",
      "delete":"Eliminar",

      "course_participants_of": "Participantes del curso",
      "curator": "CURADOR",
      "give_curator": "Otorgar credenciales de curador",
      "remove_curator": "Deponer los poderes del curador",

      "course_content": "Contenido del curso",
      "test":"Test",
      "article":"Artículo",
      "hecho":"Hecho",
      "checking": "en la verificación",
      "not_done": "No ejecutado",
      "show_summary": "Ver Resumen de progreso",
      "test_desc": "Responde a las preguntas y consigue un premio",
      "article_desc": "Lee el artículo y come un dulce",

      "course_summary": "Resumen del curso",
      "course_unit": "elemento de curso",
      "tesk_type": "Tipo",
      "status":"Status",
      "mark": "Evaluación",
      "unit":"Sección",
      "result":"Resultado",
      "unit_result": "Resumen de la partición",

      "read_article": "Artículo leído",

      "show_tries": "Ver intentos",
      "leaders_table": "tabla de clasificación",
      "progress_graphic": "Gráfico de progreso",
      "friends_progress": "Progreso de amigos",
      "last_tries": "Resultados de tus intentos anteriores",
      "try_number": "número de intento",
      "condition":"Estado",
      "viewing":"Ver",
      "time_spent": "Tiempo perdido",
      "show_try": "Ver intento",
      "best_mark":"Puntuación más Alta:",
      "best_mark_":"Puntuación Más alta",
      "place":"Lugar",
      "user":"Usuario",
      "graphic_desc": "Gráfico de la distribución de usuarios según la Puntuación más alta",
      "friends_table_desc": "clasificación de amigos a los que sigues",
      "marking_method": "Método de evaluación: Profesor",
      "start_test": "Iniciar prueba",

      "try_showing": "Ver intento",
      "information":"Información",
      "question":"Pregunta",
      "score":"Puntos:",
      "not_marked": "No evaluado",
      "the_same_answer": "los usuarios dieron la misma respuesta a esta tarea",
      "curator_comment": "Comentario del curador:",
      "your_result":"tu resultado es:",
      "your_time_spent": "ha Pasado el tiempo ",

      "passing_the_test": "Pasar la prueba",
      "complete_test": "Completar la prueba",

      "course_reviews": "Opiniones sobre el curso",

      "course_editing": "Edición del curso",
      "check":"Check",
      "editar":"Editar",
      "task_creation": "Crear una tarea",
      "choose_task_type": "Seleccione el tipo de trabajo que desea crear:",
      "confirm_delete_unit": "confirmación de eliminación de partición",
      "confirm_delete_test": "confirmación de eliminación de prueba",
      "confirm_delete_article": "confirmación de la eliminación del artículo",
      "are_u_sure_delete_unit": "definitivamente quieres eliminar la partición",
      "are_u_sure_delete_test": "definitivamente quieres eliminar la prueba",
      "are_u_sure_delete_article": "definitivamente quieres eliminar el artículo",
      "unit_creation": "crear una partición",
      "enter_unit_name": "Introduzca el nombre de la sección:",
      "save_course": "Guardar curso",

      "article_edit": "Redacción de un artículo",
      "enter_article": "Introducir un artículo (en Markdown)",
      "article_text": "Texto del artículo",
      "article_preview": "vista Previa de tu artículo",
      "save_article": "Guardar artículo",

      "article_constructor": "constructor de artículos",

      "test_checking": "Comprobación de prueba",
      "tires_results": "Resultados de los intentos",
      "check_try": "Comprobar intento",

      "test_checking_user": "Comprobación del intento del usuario",
      "add_comment": "Añadir un comentario",
      "result_":"Resultado:",
      "complete_checking": "Finalizar comprobación",

      "test_editor_of": "Editor de pruebas",
      "test_editor": "Editor de pruebas",
      "solo": "La única respuesta",
      "multiple": "respuesta Múltiple",
      "free": "Breve respuesta libre",
      "detailed_free":"respuesta Gratuita",
      "info_block": "bloque de Información",
      "add_question": "Añadir pregunta",
      "save_test": "Guardar prueba",

      "test_constructor": "constructor de pruebas",

      "access_denied": "acceso denegado",
      "but_you_can_subscribe": "pero puedes acceder a este curso suscribiéndote a él",

      "new_note":"nueva nota",
      "name_":"Nombre:",
      "note_":"Nota:",
    },
}

  $(function() {
    $('.translate').click(function() {
      var lang = $(this).attr('id');
      $('.lang').each(function(index, item) {
        $(this).text(arrLang[lang][$(this).attr('key')]);
		$('.curflag').removeClass('flag-united-kingdom').removeClass('flag-russia').removeClass('flag-germany').removeClass('flag-france').removeClass('flag-spain').addClass(arrLang[lang][$('.curflag').attr('key')]);
      });
		if (lang == "en"){
			document.getElementById("ru-tick").style.visibility = "hidden";
			document.getElementById("de-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "hidden";
			document.getElementById("es-tick").style.visibility = "hidden";
			document.getElementById("en-tick").style.visibility = "visible";
			localStorage.setItem('language', 'en')
		} else if(lang == "ru") {
			document.getElementById("ru-tick").style.visibility = "visible";
			document.getElementById("en-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "hidden";
            document.getElementById("es-tick").style.visibility = "hidden";
			document.getElementById("de-tick").style.visibility = "hidden";
			localStorage.setItem('language', 'ru')
		} else if(lang == "de") {
			document.getElementById("de-tick").style.visibility = "visible";
			document.getElementById("en-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "hidden";
            document.getElementById("es-tick").style.visibility = "hidden";
			document.getElementById("ru-tick").style.visibility = "hidden";
			localStorage.setItem('language', 'de')
		} else if(lang == "fr") {
			document.getElementById("de-tick").style.visibility = "hidden";
			document.getElementById("en-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "visible";
            document.getElementById("es-tick").style.visibility = "hidden";
			document.getElementById("ru-tick").style.visibility = "hidden";
			localStorage.setItem('language', 'fr')
		} else if(lang == "es") {
			document.getElementById("de-tick").style.visibility = "hidden";
			document.getElementById("en-tick").style.visibility = "hidden";
			document.getElementById("fr-tick").style.visibility = "hidden";
            document.getElementById("es-tick").style.visibility = "visible";
			document.getElementById("ru-tick").style.visibility = "hidden";
			localStorage.setItem('language', 'es')
		}
    });
  });

  let lang = localStorage.getItem('language');
  if(lang.valueOf() == 'en'.valueOf()){
      document.getElementById("ru-tick").style.visibility = "hidden";
      document.getElementById("de-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "hidden";
      document.getElementById("en-tick").style.visibility = "visible";
  } else if(lang.valueOf() == 'ru'.valueOf()){
      document.getElementById("ru-tick").style.visibility = "visible";
      document.getElementById("en-tick").style.visibility = "hidden";
      document.getElementById("de-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "hidden";
  } else if(lang.valueOf() == 'de'.valueOf()){
      document.getElementById("de-tick").style.visibility = "visible";
      document.getElementById("en-tick").style.visibility = "hidden";
      document.getElementById("ru-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "hidden";
  } else if(lang.valueOf() == 'fr'.valueOf()){
      document.getElementById("de-tick").style.visibility = "hidden";
      document.getElementById("en-tick").style.visibility = "hidden";
      document.getElementById("ru-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "visible";
  } else if(lang.valueOf() == 'es'.valueOf()){
      document.getElementById("de-tick").style.visibility = "hidden";
      document.getElementById("en-tick").style.visibility = "hidden";
      document.getElementById("fr-tick").style.visibility = "hidden";
      document.getElementById("es-tick").style.visibility = "visible";
      document.getElementById("ru-tick").style.visibility = "hidden";
  }
  $('.lang').each(function(index, item) {
      $(this).text(arrLang[lang][$(this).attr('key')]);
      $('.curflag').removeClass('flag-united-kingdom').removeClass('flag-russia').removeClass('flag-germany').removeClass('flag-france').removeClass('flag-spain').addClass(arrLang[lang][$('.curflag').attr('key')]);
  });