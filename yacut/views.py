from random import choice
import string

from flask import flash, redirect, render_template
from http import HTTPStatus

from . import app, db
from .forms import URLMapForm
from .models import MAX_LEN_CUSTOM_ID, URLMap


def get_unique_short_id():
    return ''.join([choice(string.ascii_letters + string.digits) for _ in range(6)])


@app.route('/', methods=['GET', 'POST'])
def link_shorter_view():
    form = URLMapForm()
    if form.validate_on_submit():
        original_link = form.original_link.data
        custom_id = form.custom_id.data
        if URLMap.query.filter_by(original=original_link).first():
            flash('Имя {} уже занято!'.format(custom_id))
            return render_template('index.html', form=form)
        if URLMap.query.filter_by(short=custom_id).first():
            flash('Имя {} уже занято!'.format(custom_id))
            return render_template('index.html', form=form)
        if form.custom_id.data:
            if len(form.custom_id.data) > MAX_LEN_CUSTOM_ID:
                flash('Ссылка не должна превышать 16 символов')
                return render_template('index.html', form=form)
            custom_id = form.custom_id.data
        else:
            custom_id = get_unique_short_id()

        urlmap = URLMap(
            original=form.original_link.data,
            short=custom_id,

        )
        db.session.add(urlmap)
        db.session.commit()
        return render_template('index.html', form=form, context=urlmap)
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET'])
def new_link_view(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first_or_404()
    return redirect(urlmap.original, code=HTTPStatus.FOUND)
