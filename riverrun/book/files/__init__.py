from . import epub


PARSERS = {
    ext: mod.File
    for mod in (
        epub,
    )
    for ext in getattr(mod.File, 'extensions', (mod.File.extension,))
}

def parse(f):
    if isinstance(f, str):
        f = open(f, 'rb')
    ext = f.name.rsplit('.', 1)[1].lower()
    try:
        return PARSERS[ext](f)
    except KeyError:
        raise ValueError('Unsupported file extension {}'.format(ext))
