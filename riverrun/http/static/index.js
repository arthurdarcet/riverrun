Riverrun.Collections = {};
Riverrun.Views = {};

Riverrun.Views.Book = Backbone.View.extend({
    events: {
    },

    initialize: function() {
        this.model.on('change', _.bind(this.render, this));
        this.render();
    },

    render: function(append) {
        var html = Riverrun.templates.book(this.model.attributes);
        var old_el = this.$el;
        this.setElement(html);
        old_el.replaceWith(this.$el);
    }
});

Riverrun.Collections.Books = Backbone.Collection.extend({
    initialize: function() {
        this.container = $('.books');

        this.on('add', _.bind(function(model) {
            model.view = new Riverrun.Views.Book({model: model});
            this.container.append(model.view.$el);
        }, this));
    },

    refresh: function() {
        $.ajax({
            type: 'GET',
            url: '/books',
            context: this
        }).done(function(data, status) {
            this.add(data);
        });
    }
});

$(document).ready(function() {
    Riverrun.templates = {
        book: Handlebars.compile($('#book-template').html())
    };
    Riverrun.books = new Riverrun.Collections.Books();

    Riverrun.books.refresh();
});
