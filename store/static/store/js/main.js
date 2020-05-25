// $(document).ready(function(){
//     $('form').on('submit', function(event) {
//         $.ajax({
//             data : {
//                 button : $('#save').val()
//             },
//             type : 'GET', 
//             url : '/'
//         })
//         .done(function(data) {
//             if (data.is_favorite === True) {
//                 $('.form-save').update(`
//                     <button name='button-save' type='submit'><i id='save' class="far fa-save" aria-hidden="true"></i> Supprimer des favoris</button>
//                 `)
//             };
//         })
//     })
// })