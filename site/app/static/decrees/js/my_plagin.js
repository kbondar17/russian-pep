
// const session = document.URL 123123
// const session = document.getElementById('session').value



// function get_files_promise() {
//     const url = `http://localhost:8010/proxy/work/${session}/all`
//     return new Promise((resolve, reject) => {
//         fetch(url, {
//             retries: 3,
//             retryDelay: 1000,
//             retryOn: function (attempt, error, response) {
//                 // retry on any network error, or 4xx or 5xx status codes
//                 if (error !== null || response.status >= 400) {
//                     console.log(`retrying, attempt number ${attempt + 1}`);
//                     return true;
//                 }
//             }
//         }).then(resp => {
//             if (resp.status == 200) {
//                 resolve(resp.json())

//             } else {
//                 reject(new Error(`ошибка на сайте ${resp.statusText}`))
//             }
//         }).catch(resp => reject(new Error(`catched ошибка на сайте --- ${resp}`))
//         )
//     })
// }


// function generate_file_table() {
//     let promise = get_files_promise()

//     return new Promise((resolve, reject) => {
//         promise.then(
//             (result) => {
//                 // console.log(`${JSON.stringify(result)} загружен!`)
//                 return result//JSON.parse(result)
//             },
//             (error) => {
//                 console.log(`Ошибка: ${error}`)
//                 reject(new Error('Нет файлов!'))

//             }).then((all_files) => {
//                 if (Object.keys(all_files).length < 1) {
//                     reject(new Error('Нет файлов!'))
//                 }

//                 const table = document.getElementsByClassName('file_table')[0]
//                 // console.log('Полученные в generate_file_table файлы---')

//                 for (let i = 0; i < all_files.length; i++) {
//                     let filename = all_files[i]['filename']
//                     // console.log(filename)

//                     const file_html_template = `
//                             <tr>
//                             <th scope="row">${i + 1}</th>
//                             <td id="download_table_cell" data-toggle="tooltip" data-placement="top"
//                             title="${filename}">
//                                 <p data-toggle="tooltip" data-placement="top"
//                                 title="${filename}">${filename.slice(0, 66)}</p>
//                             </td>
//                             <td id="download_table_cell">?? Mb</td>
//                             <td id="download_table_cell">
//                                 <div name='${filename}' data-loaded='false'>

//                                 <div style="height:100%; width: 180%;" data-preset="stripe"
//                                         id="progress_bar" class="ldBar label-center"
//                                          data-value="10">
//                                     </div>

//                             </td>
//                         </tr>  `

//                     table.insertAdjacentHTML('beforeend', file_html_template)

//                 }
//                 resolve('Создали табл')
//             }
//             )
//     }
//     ).catch((err) => {
//         console.log('поймали ошибку', err)

//     })
// }


// function get_files_from_cookies() {
//     // get cookie
//     function getCookie(name) {
//         let matches = document.cookie.match(new RegExp(
//             "(?:^|; )" + name.replace(/([\.$?*|{}\(\)\[\]\\\/\+^])/g, '\\$1') + "=([^;]*)"
//         ));
//         return matches ? decodeURIComponent(matches[1]) : undefined;
//     }


//     let total_files_number = getCookie('total_files')

//     let all_files = Array()
//     for (let i = 0; i < total_files_number; i++) {
//         let user_file = getCookie(`filename_${i}`)
//         all_files.push(user_file)

//     }
//     return all_files

// }

// function generate_table_from_files(files) {
//     const table = document.getElementsByClassName('file_table')[0]

//     for (let i = 0; i < files.length; i++) {
//         let file = files[i]
//         file = file.replace(/^"+|"+$/g, '').trim()

//         const file_html_template = `
//         <tr>
//         <th scope="row">${i + 1}</th>
//         <td id="download_table_cell" data-toggle="tooltip" data-placement="top"
//         title="${file}">
//             <p data-toggle="tooltip" data-placement="top"
//             title="${file}">${file.slice(0, 66)}...</p>
//         </td>
//         <td id="download_table_cell">?? Mb</td>
//         <td id="download_table_cell">
//             <div name='${file}' data-loaded='false'>

//             <div class="progress">
//                 <div class="progress-bar progress-bar-striped active" role="progressbar" aria-valuenow="90"
//                     aria-valuemin="0" aria-valuemax="100" style="width:1%">

//                 </div>
//             </div>

//         </td>
//     </tr>  `

//         table.insertAdjacentHTML('beforeend', file_html_template)

//     }
// }




// function move_progress_bar() {
//     console.log('вошли в прогресс')
//     function getRandomInt(max) {
//         return Math.floor(Math.random() * max);
//     }

//     let bars = document.getElementsByClassName('progress-bar')

//     setInterval(() => {
//         for (let i = 0; i < bars.length; i++) {
//             let bar = bars[i]

//             let bar_val = Number(bar.attributes.style.value.split(':')[1].replace('%', ''))
//             if (bar_val < 91) {
//                 let new_val = bar_val + getRandomInt(10)
//                 bar.attributes.style.value = `width:${new_val}%`
//             }


//             console.log(bar_val)
//             //= 'width:100%'
//             // let bar_val = window.getComputedStyle(bar)['width']

//         }
//     }, 1000)

// }

// function update_files_status() {
//     const url = `http://localhost:8010/proxy/work/${session}/finished`

//     setInterval(() => {
//         return fetch(url).then((resp) => {
//             return resp.json()
//         }).then((res) => {
//             console.log('res---', res)
//             if (res) {
//                 for (let i = 0; i < res.length; i++) {
//                     let filename = res[i]['filename'] //.replace('.xlsx', '')
//                     console.log('finished filename---', filename)

//                     let el = document.querySelector(`div[name="${filename}"]`)
//                     if (!el) {
//                         continue
//                     } else {
//                         if (el.dataset.loaded == 'false') {

//                             let el_bar = el.querySelector('div')
//                             el_bar.ldBar.set(100)

//                             let download_url = 'http://127.0.0.1:5000/' + res[i]['link']


//                             let download_link = document.createElement('a')
//                             download_link.setAttribute('href', download_url)
//                             download_link.innerHTML = 'скачать'
//                             el.replaceWith(download_link)
//                             el.dataset.loaded = true

//                         }

//                     }

//                 }
//             }

//         })
//     }, 1000)
// }

// let all_files = get_files_from_cookies()
// generate_table_from_files(all_files)
// move_progress_bar()



// $(window).on('load', function () {
//     alert('loaded')
// }


// function window_switcher(href) {

//     // найти окно-цель
//     href = href.split('/')

//     let id_ = href[0]
//     // let path_to_id = href[1]
//     let path = '/' + href[2]

//     path = path.replace(/^,+|,+$/g, '');

//     let current_nav_el = document.getElementById(`${id_}`)

//     let leaving_el = document.getElementsByClassName('nav-item active')[0]

//     console.log('leaving_el--', leaving_el)


//     leaving_el.classList.remove('active')

//     console.log('leaving_el after--', leaving_el)

//     current_nav_el.classList.add('active')

//     console.log('current_nav_el--', current_nav_el)

//     // let el_to_go = document.getElementById(`${path_to_id}`)


//     // console.log(el_to_go)
//     // console.log('current_nav_el--', current_nav_el.classList)
//     // current_nav_el.classList.add('active')
//     // console.log('curr el', current_nav_el)

//     window.location.href = `http://127.0.0.1:5555${path}`;


// }
function window_switcher() { }

addEventListener('click', (event) => {

    console.log('el class list', event.target.dataset['href'])
    let path = event.target.dataset['href']
    window.location.href = `http://127.0.0.1:5555${path}`;
    // event.target.classList.add('active')
    // event.target.classList.remove('active')
    // console.log('el class list after', event.target.classList)

    // console.log('event----', event.target.classList.remove('active'))

})

function test() {
    let path = window.location.pathname

    console.log('path--', path)
    let prev_el = document.getElementsByClassName('nav-item active')[0]
    console.log('prev_el--', prev_el)

    prev_el.classList.remove('active')

    let el = document.getElementById(path)
    console.log('target nav el--', el)

    el.classList.add('active')
    // console.log('el class--', el.classList)


}

// let html = `
//     <div class='', data-ЧТО-НИБУЛЬ='ЗНАЧЕНИЕ'>
// `

// // то что сверху можно найти по клику
// document.addEventListener('click', function (event) {
//     console.log(event.target.dataset.data.ЧТО НИБУДЬ)
// }
// )

// $(window).on('load', function () {
//     var current_path = location.pathname;
//     console.log('current---', current_path);
//     let nav_els = document.getElementsByClassName('nav-item')

//     // console.log('nav_els--', nav_els)
//     for (let i = 0; i < nav_els.length; i++) {
//         let el_href = nav_els[i].querySelector('a').dataset['href']
//         if (el_href == current_path) {
//             nav_els[i].classList.add('active')
//         }

//     }

    // $('#navbarSupportedContent ul li a').each(function () {
    //     var $this = $(this);
    //     // if the current path is like this link, make it active
    //     if ($this.attr('href').indexOf(current) !== -1) {
    //         $this.parent().addClass('active');
    //         $this.parents('.menu-submenu').addClass('show-dropdown');
    //         $this.parents('.menu-submenu').parent().addClass('active');
    //     } else {
    //         $this.parent().removeClass('active');
    //     }
    // })

    // Я молодец - понянл немного промисы. теперь надо сделать:
// 1. добавить названия файлов в сессию (мб прикрутив айдишник?)
// 2. поменять колбаску загрузки
// 3. сделать конспект, всего что узнал


// function test_bar() {


//     let res = [1, 2, 3, 4, 5]
//     for (let i = 0; i < res.length; i++) {

//         let test_file_html_template = `
//                 <h1>AAAAAAAAAAAA</h1>
//                 <div style="height:10%; width: 18%;" data-preset="stripe"
//                         id="progress_bar" class="ldBar"
//                         data-value="10">
//                     </div>

//  `
//         let el = document.createElement('div')
//         el.innerHTML = test_file_html_template
//         let test_table = document.getElementsByClassName('test_el')[0]
//         test_table.appendChild(el)
//         // document.body.insertBefore(el, test_table)
//         // console.log('вставили ряд --', i)


//         // let filename = 'its a file name уиииии'
//         // test_table.insertAdjacentHTML('beforeend', test_file_html_template)
//     }


// }



// generate_file_table().then((res) => {

//     console.log('Результат создания таблицы::', res)
//     // move_progress_bar()
//     // update_files_status()
// })

