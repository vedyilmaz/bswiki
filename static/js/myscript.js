var ib = document.querySelector("#input_search")
ib.addEventListener('change',function(){
    console.log("searching a topic!")
    window.location.replace('http://localhost:8000/article/dashboard?csrfmiddlewaretoken=OTFGS1o3NZXxzQjw4Um9N0WESKp16jj4T8kINOk57GoMeZ5YfnyGlhHaFIylhJiy&keyword=' + ib.value);
})

