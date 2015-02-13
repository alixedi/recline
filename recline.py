from bottle import template, route, run, request
from imp import load_source
from argparse import ArgumentParser
from os.path import basename, splitext
from subprocess import check_output
import os



class ScriptRender(object):
	"""Render a script as an HTML page."""

	def __init__(self, script):
		self.script = script

	def render(self):
		return template(self.get_template(), {'self': self})

	def get_template(self):
		return 'page'

	def get_title(self):
		title, _ = splitext(basename(self.script))
		return title

	def get_argparsers(self):
		mod = load_source('', self.script)
		f = lambda x: isinstance(x, ArgumentParser)
		return  filter(f, mod.__dict__.values())

	def render_argparser(self, argparser):
		return ArgparserRender(argparser).render()



class ArgparserRender(object):
	"""Render an argparse object as an HTML form."""

	def __init__(self, argparser):
		self.argparser = argparser

	def render(self):
		return template(self.get_template(), {'self': self})

	def get_template(self):
		return 'form'

	def get_description(self):
		return self.argparser.description

	def get_groups(self):
		return self.argparser._action_groups

	def render_group(self, group):
		return GroupRender(group).render()

	def get_epilog(self):
		return self.argparser.epilog



class GroupRender(object):
	"""Render an action group as an HTML formset."""

	def __init__(self, group):
		self.group = group

	def render(self):
		return template(self.get_template(), {'self': self})

	def get_template(self):
		return 'formset'

	def get_title(self):
		return self.group.title

	def get_actions(self):
		actions = self.group._group_actions
		no_help = lambda a: not type(a).__name__ == '_HelpAction'
		return filter(no_help, actions)

	def render_action(self, action):
		return ActionRender(action).render()



class ActionRender(object):
	"""Render an action as an HTML field."""

	def __init__(self, action):
		self.action = action

	def render(self):
		return template(self.get_template(), {'self': self})

	def get_template(self):
		return 'field'

	def get_flag(self):
		opt = self.action.option_strings
		if len(opt) > 0:
			return opt[0]
		return None

	def get_name(self):
		flag = self.get_flag()
		if flag:
			return flag.strip('-')
		return self.action.dest

	def get_required(self):
		return 'required' if self.action.required else ''

	def get_default(self):
		value = self.action.default
		if hasattr(value, '__call__'):
			return value.__name__
		return value

	def get_help(self):
		return self.action.help

	def get_type(self):
		kls = type(self.action).__name__
		fmt = '_Store%sAction'
		if kls in [fmt % x for x in ('Const', 'True', 'False')]:
			return 'checkbox'
		elif kls == '_StoreAction':
			typ = self.action.type.__name__
			mpg = {'int': 'number',
				   'file': 'file'}
			if typ in mpg:
				return mpg[typ]
			return ''


@route('/')
def send_form():
	return __R__.render()

@route('/', method='POST')
def process_form():
	args = []
	for argparser in __R__.get_argparsers():
		argparser_render = ArgparserRender(argparser)
		for group in argparser_render.get_groups():
			group_render = GroupRender(group)
			for action in group_render.get_actions():
				action_render = ActionRender(action)
				name = action_render.get_name()
				value = request.forms.get(name)
				if value:
					flag = action_render.get_flag()
					if flag:
						args = args + [flag]
					args = args + [value]
	print ['python'] + [__R__.script] + args
	return check_output(['python'] + [__R__.script] + args)


parser = ArgumentParser(description='Web Apps from CLI scripts.')
parser.add_argument('script', type=file)

if __name__ == '__main__':
	args = parser.parse_args()
	global __R__
	__R__ = ScriptRender(args.script.name)
	run(host='localhost', port=8080)