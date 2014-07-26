from herzog.base.exception import FormValidError, HZActionError
from herzog.base.misc import json_error
from herzog.base.app import request
from functools import wraps

def ajax_fields_error(f):
    @wraps(f)
    def wrapper():
        try :
            return f()
        except FormValidError as e:
            return json_error(1, e.message, params=e.params)
        except HZActionError as e:
            return json_error(3, e.message)
    return wrapper

def getfields(_require, _optional=(), _form=None, **typer) :
    if _form is None :
        _form = request.form
    ret = {}
    missing = []
    if _require :
        for name in _require :
            field = _form.get(name, None)
            if not field :
                missing.append(name)
                continue
            if name in typer :
                try :
                    ret[name] = typer[name](field)
                except (TypeError, ValueError) :
                    raise FormValidError('Wrong %s value' % name,
                                         name=name, value=_form.get(value))
                continue
            ret[name] = field
    if _optional :
        for name in _optional :
            field = _form.get(name, None)
            if not field :
                continue
            if name in typer :
                try :
                    ret[name] = typer[name](field)
                except (TypeError, ValueError) :
                    raise FormValidError('Wrong %s value' % name,
                                         name=name, value=_form.get(value))
                continue
            ret[name] = field
    if missing :
        raise FormValidError('Missing params: %s' % (','.join(missing)),
                             missing=missing)
    return ret
