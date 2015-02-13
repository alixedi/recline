% name = self.get_name()
<label>{{ name }}</label>
<input  {{ self.get_required() }}
    id="{{ name }}"
    name="{{ name }}"
    value="{{ self.get_default() }}"
    placeholder="{{ self.get_help() }}"
    type="{{ self.get_type() }}">
<br>