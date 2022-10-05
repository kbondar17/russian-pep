// let test_session = '2b88818c9e8511ae74d9add26c7e9d5380a2ae7c2eee4d9ca84d0649'
let test_session = '444'



function update() {
    let u_range = [5, 6, 7, 8, 9]

    let interval = setInterval(() => {
        for (let i = 0; i < u_range.length; i++) {
            console.log('updating val', i)
            if (true) {
                clearInterval(interval)
                return 'update value'

            }
        }
    }, 1400)


}

function move_bar() {
    let range = [1, 2, 3]
    let iteration = 0
    let interval = setInterval(() => {
        for (let i = 0; i < range.length; i++) {
            console.log('moving bar', i)
            iteration += 1
            console.log('bar iteration---', iteration)

            if (iteration > 3) {
                clearInterval(interval)
                return 'move_bar value'

            }

        }

        // console.log('обновляем')
    }, 2000)

}

const my_fun = () => {
    const promise = new Promise((resolve, reject) => {
        setTimeout(() => {
            let recieved_files = get_files()
            console.log('recieved_files---', recieved_files)
            console.log('recieved_files bool ---', Boolean(recieved_files))

            if (recieved_files) {
                resolve(recieved_files)
            } else {
                reject('файлов нет')
            }

        }, 3000)

    })
    return promise
}

function get_files_promise() {
    const url = `http://localhost:8010/proxy/work/${test_session}/all`
    // const test_url = 'https://api.github.com/repos/javascript-tutorial/en.javascript.info/commits'
    return new Promise((resolve, reject) => {
        fetch(url, {
            retries: 3,
            retryDelay: 1000,
            retryOn: function (attempt, error, response) {
                // retry on any network error, or 4xx or 5xx status codes
                if (error !== null || response.status >= 400) {
                    console.log(`retrying, attempt number ${attempt + 1}`);
                    return true;
                }
            }
        }).then(resp => {
            if (resp.status == 200) {
                resolve(resp.json())

            } else {
                reject(new Error(`ошибка на сайте ${resp.statusText}`))
            }
        }).catch(resp => reject(new Error(`catched ошибка на сайте --- ${resp}`))
        )
    })
}




let promise = get_files_promise()
promise.then(
    result => console.log(`${JSON.stringify(result)} загружен!`),
    error => alert(`Ошибка: ${error}`)
).catch(resp => alert(`последний catch -- ${resp}`)).then(() => {
    update(),
        move_bar()

})



// function retry() {
//     const test_url = 'https://api.github.com/repos/javascript-tutorial/en.javascript.info/commits'
//     let i = 0
//     let found = false
//     let site_resp = fetch(test_url)

//     // while (!found) {
//     site_resp.then(resp => {
//         console.log('пошли на сайт')
//         if (resp.status == 200) {
//             console.log('res == 200')
//             found = true
//             return resp.json()
//         } else {
//             console.log('net')
//         }

//     }
//     ).then(res => console.log('получили'))
//     // }

// }
// retry()

// const fetchPromise = fetch(test_url)

    // fetchPromise.then(resp => {
    //     return resp.json()
    // }).then(res => {
    //     console.log(res)
    // })


    // const promise = new Promise((resolve, reject) => {
    //     fetch(test_url)
    //         .then((response) => {
    //             if (response.status == 200) {
    //                 console.log('все ок!')
    //                 response.json()
    //             } else {
    //                 alert('пизда')
    //                 reject(new Error('ошибка'))
    //                 return 'пиздец'
    //             }
    //         }
    //         )
    //         .then((res) => {
    //             console.log('second then --', res)
    //             resolve(res)
    //         }
    //         )
    //     // .catch(mess => alert(`catch ошибку -- ${mess}`), reject('catched err'));

    // })
    // return promise


// console.log('get_files_promise--', get_files_promise()
//     .then(res => console.log(res)))

// my_fun().then(
//     res => console.log('res in then --', res),

// ).catch(err => console.error('ОШИБКАА:', err))

// delay(2500)
//   .then(() => {
//     console.log('After 2 seconds')
//   })
//   .catch(err => console.error('Error:', err))
//   .finally(() => console.log('Finally'))

// let promise = new Promise(function (resolve, reject) {
//     const recieved_files = get_files()
//     if (recieved_files) {
//         console.log('получили файлы---', recieved_files)
//         resolve(files)
//     } else {
//         reject(new Error('файлов нет!'))
//     }

// })

// promise.then(
//     function (result(t)) => {
//         console.log('действительно получили файлы. вот они --', t)
//     },
//     function (reject) {

//     }
// )


// get_files().then(function (files) {

//     // function get_two_values() {
//     //     let up_val = update()
//     //     let bar_val = move_bar()
//     //     return bar_val
//     // }
//     // let res = get_two_values()
//     // get_two_values().then((res) => { return res })


// }).then((res) => {
//     console.log('Завершили!. res -- ', res)
// })


