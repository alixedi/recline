<legend>{{ !self.get_title() }}</legend>
% for action in self.get_actions():
  {{ !self.render_action(action) }}
% end
