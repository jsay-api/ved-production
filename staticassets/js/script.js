var main = function() {
    /*$('.login').click(function() {
      $('.login .dropdown-menu').toggle();
    });*/

    var searchText = "";
    var csrftoken = null;
    /*var active = null;*/
    var url = "";
    var tabs = [{
            name: '.tab0',
            url: '/BO/'
        },
        {
        	name: '.tab1',
        	url: '/AB/'
        },
        {
        	name: '.tab2',
        	url: '/AO/'
        }];

    tabs.forEach(function(tab){
        $('#ajax-content').on('click', tab.name, search(tab.url));
    })

    $('.menu').click(function() {
        $('.menu .dropdown-menu').toggle();
    });

    function search(url) {
    	csrftoken = $('input[name=csrfmiddlewaretoken]').val();
        return function(event) {
            $.ajax({
                type: "POST",
                url: url,
                data: {
                    'query': searchText
                },
                //setting header for scrf-protection
                beforeSend: function(xhr) {
                    xhr.setRequestHeader("X-CSRFToken", csrftoken);
                },
                //function running if success
                success: function(response) {
                    //show responded html
                    console.log('success');
                    $('#ajax-content').html(response.html);
                },
                error: function(xhr, status, error) {
                    console.log('error = ', error);
                }
            });

        };
    };

    $('#sch').submit(function(event) {
        var query = $('#Search').val();
        searchText = query;
        var active = '.'+($('.active').children().attr('class'));
        console.log(active);
        for (var i = tabs.length - 1; i >= 0; i--) {
        	if (tabs[i].name == active) {
        		url = tabs[i].url;
        	};
        };
        console.log(url);
        search(url)();
        /*$('#ajax-content').on('click', active, search(url));*/
        return false;
    });
};
$(document).ready(main);