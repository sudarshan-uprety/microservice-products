def get_obj_or_404(model, id) -> object:
    obj = model.objects.get(id=id)
    return obj
