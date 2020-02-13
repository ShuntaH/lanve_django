from django import forms


class FileInputWithPreview(forms.FileInput):
    """プレビュー表示されるinput type=file"""
    template_name = 'widgets/file_input_with_preview.html'
    initial_text = 'Currently'

    class Media:
        js = ['lanve/js/preview.js']

    def __init__(self, attrs=None, include_preview=True):
        super().__init__(attrs)
        if 'class' in self.attrs:
            self.attrs['class'] += 'preview-marker'
        else:
            self.attrs['class'] = 'preview-marker'
        self.include_preview = include_preview
        if attrs is not None:
            attrs = attrs.copy()
            self.input_type = attrs.pop('type', self.input_type)
        super().__init__(attrs)

    def is_initial(self, value):
        """
        Return whether value is considered to be initial value.
        """
        return bool(value and getattr(value, 'url', False))

    def format_value(self, value):
        """
        Return the file object if it has a defined url attribute.
        """
        if self.is_initial(value):
            return value

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget'].update({
            'include_preview': self.include_preview,
            'is_initial': self.is_initial(value),
            'initial_text': self.initial_text,
        })
        return context
