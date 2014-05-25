Riverrun.Collections = {};
Riverrun.Views = {};


Riverrun.Collections.Books = Backbone.Collection.extend({
    url: '/books',
    current_page: -1,
    params: {},

    initialize: function() {
        this.container = $('.books');

        this.on('add', _.bind(function(model) {
            var el = Riverrun.templates.book(model.attributes);
            this.container.append(el);
        }, this));
    },

    load_next_page: function(page) {
        if (this.loading) {
            return;
        }

        this.current_page++;
        this.loading = true;

        $.ajax({
            type: 'GET',
            url: this.url + '?' + $.param(_.extend({page: this.current_page}, this.params)),
            context: this
        }).done(function(data, status) {
            if (this.current_page == 0) {
                this.container.html('');
                this.reset();
            }
            this.add(data);
            this.loading = false;
        });
    },

    search: function(q) {
        if (q) {
            this.url = '/search';
            this.params.q = q;
        }
        else {
            this.url = '/books';
            this.params = {};
        }
        this.current_page = -1;
        this.load_next_page();
    }
});

Riverrun.Views.SearchBar = Backbone.View.extend({
    el: '.search input',
    events: {
        'keyup': 'keyup',
    },

    keyup: function(evt) {
        evt.preventDefault();
        if (evt.keyCode == 13 || Riverrun.books.params.q != this.$el.val()) {
            Riverrun.books.search(this.$el.val());
        }
    }
});

$(document).ready(function() {
    Riverrun.templates = {
        book: Handlebars.compile($('#book-template').html())
    };
    Riverrun.books = new Riverrun.Collections.Books();
    Riverrun.search_bar = new Riverrun.Views.SearchBar();

    Riverrun.books.load_next_page();
    $(window).scroll(function(){
        if ($(window).scrollTop() >= $(document).height() - $(window).height() - 200) {
            Riverrun.books.load_next_page();
        }
    });
});
