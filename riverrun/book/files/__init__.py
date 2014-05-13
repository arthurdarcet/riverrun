from . import epub


PARSERS = {
    mod.File.extension: mod.File
    for mod in (
        epub,
    )
}

def parse(f):
    ext = f.name.rsplit('.', 1)[1].lower()
    try:
        return PARSERS[ext](f)
    except KeyError:
        raise ValueError('Unsupported file extension {}'.format(ext))
