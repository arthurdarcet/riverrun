Riverrun.Collections = {};
Riverrun.Views = {};

Riverrun.Views.Book = Backbone.View.extend({
    events: {
    },

    initialize: function() {
        this.model.on('change', _.bind(this.render, this));
        this.render();
    },

    render: function() {
        var html = Riverrun.templates.book(this.model.attributes);
        var old_el = this.$el;
        this.setElement(html);
        old_el.replaceWith(this.$el);
    }
});

Riverrun.Collections.Books = Backbone.Collection.extend({
    url: '/books',
    current_page: -1,

    initialize: function() {
        this.container = $('.books');

        this.on('add', _.bind(function(model) {
            model.view = new Riverrun.Views.Book({model: model});
            this.container.append(model.view.$el);
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
            url: this.url + '?' + $.param({page: this.current_page}),
            context: this
        }).done(function(data, status) {
            this.add(data);
            this.loading = false;
        });
    }
});

$(document).ready(function() {
    Riverrun.templates = {
        book: Handlebars.compile($('#book-template').html())
    };
    Riverrun.books = new Riverrun.Collections.Books();

    Riverrun.books.load_next_page();
    $(window).scroll(function(){
        if ($(window).scrollTop() >= $(document).height() - $(window).height() - 200) {
            Riverrun.books.load_next_page();
        }
    });
});
