
@given(u'we want to add a product')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given we want to add a product')


@when(u'we fill in the form')
def step_impl(context):
    raise NotImplementedError(u'STEP: When we fill in the form')


@then(u'it succeeds')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then it succeeds')


@given(u'we have specific products to add')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given we have specific products to add')


@when(u'we visit the listing page')
def step_impl(context):
    raise NotImplementedError(u'STEP: When we visit the listing page')


@then(u'we will find \'another thing\'')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then we will find \'another thing\'')
