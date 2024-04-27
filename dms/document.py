import os.path
from datetime import datetime, timezone
from mimetypes import guess_type
from uuid import uuid4

from flask import (Blueprint, abort, current_app, flash, g, redirect,
                   render_template, request, send_from_directory)
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, NoResultFound
from werkzeug.utils import secure_filename

from .auth import login_required
from .models import Document

FILE_UPLOAD_PATH = r"d:\projects\fitproject\instance\uploads"

bp = Blueprint('document', __name__, url_prefix='/doc')


@bp.route('/upload', methods=('GET', 'POST'))
@login_required
def upload_file():
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file uploaded.")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash("No file attached.")
            return redirect(request.url)
        mime = file.mimetype or guess_type(
            file.filename) or "application/octet-stream"
        filename = secure_filename(file.filename)
        uuid = uuid4()
        uploaded = datetime.now(tz=timezone.utc)
        print(g.user)
        document = Document(id=uuid, name=filename,
                            uploaded=uploaded, mime=mime, owner=g.user)
        session = current_app.db.session
        try:
            session.add(document)
            file.save(os.path.join(FILE_UPLOAD_PATH, str(uuid)))
            session.commit()
        except (IntegrityError, FileExistsError, FileNotFoundError) as e:
            session.rollback()
            flash(f"Error uploading file. {e}")
            return redirect(request.url)
        else:
            flash("File uploaded.")
            return redirect(request.url)

    return render_template("document/upload.html")


@bp.route("/download/<id>", methods=['GET'])
def download_file(id):
    try:
        session = current_app.db.session
        query = select(Document).where(Document.id == id)
        document = session.scalars(query).one()
        return send_from_directory(
            FILE_UPLOAD_PATH, str(document.id), mimetype=document.mime,
            download_name=document.name, last_modified=document.uploaded)
    except NoResultFound:
        abort(404)
