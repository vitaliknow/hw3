class TextHistory:
	def __init__(self):
		self._text = ''
		self._length = 0
		self._version = 0
		self._Actions = {}

	@property
	def text(self):
		return self._text
	@property
	def version(self):
		return self._version
		
	def action(self, action):
		if (action.isVersions_False(self._version)) or (action.apply(self._text) == False):
			raise ValueError
		self._text = action.apply(self._text)
		self._length = len(self._text)
		if action.to_version  == 0:
			self._version += 1
			action.to_version = self._version
		else:	
			self._version = action.to_version
			
		self._Actions[self._version] = action
		return self._version
		
	def insert(self, text_to_I, pos = None):
		if pos == None:
			pos = self._length
		elif (0 > pos and pos > self._length):
			raise ValueError
		return self.action(InsertAction(pos, text_to_I, self._version))
			
	def replace(self, text_toR, pos = None):
		if pos == None:
			pos = self._length
		if pos < 0:
			raise ValueError
		return self.action(ReplaceAction(pos, text_toR, self._version))
		
	def delete(self, pos, length):
		if (0 < pos > self._length):
			raise ValueError
		return self.action(DeleteAction(pos, length, self._version))
		
	def get_actions(self, v1 = 0, v2 = 0):
		if (v1 > v2 and v2!=0) or v1 < 0 or v2 > self._version:
			raise ValueError

		'''
		merged_Actions = {}
		prev_action = None
		for j in self._Actions:
			merged_Actions[j] = merge(prev_action, self._Actions[j])
			prev_action = self._Actions[j]
		self._Actions = merged_Actions
		'''

		list_to_return = []
		for i in self._Actions:
			if ((v2==0 and v1!=0 and i>v1) or (v1 <= i <= v2)):
				list_to_return.append(self._Actions[i])
		
		return list_to_return

class Action:
	def __init__ (self, pos = 0, from_version = 0, to_version = 0):
		self.pos = pos
		self.from_version = from_version
		self.to_version = to_version
		
	def apply(self, text = ''):
		pass

	def isVersions_False(self, ver_of_TH):
		if ((self.from_version >= self.to_version)and(self.to_version != 0) or self.from_version < 0 or self.from_version != ver_of_TH):
			return True
		else:
			return False

class InsertAction(Action):
	def __init__ (self, pos = 0, text = '', from_version = 0, to_version = 0):
		super().__init__(pos, from_version, to_version)
		self.text = text

	
	def apply(self, text = ''):
		if self.pos > len(text) or self.pos < 0:
			return False
		pos = self.pos
		return (text[:pos] + self.text + text[pos:])

class ReplaceAction(Action):
	def __init__ (self, pos = 0, text = '', from_version = 0, to_version = 0):
		super().__init__(pos, from_version, to_version)
		self.text = text
		
	def apply(self, text):
		if self.pos > len(text):
			return False
		pos1 = self.pos
		pos2 = pos1 + len(self.text)
		return (text[:pos1] + self.text + text[pos2:])

class DeleteAction(Action):
	def __init__ (self, pos, length, from_version = 0, to_version = 0):
		super().__init__(pos, from_version, to_version)
		self.length = length
	
	def apply(self, text):
		if (self.pos + self.length > len(text)) or self.pos < 0:
			return False
		pos1 = self.pos
		pos2 = self.pos + self.length
		return text[:pos1] + text[pos2:]

def merge(action1, action2):
		
	if (type(action1) == type(action2) == InsertAction):
		pos1, pos2 = action1.pos, action2.pos
		text1, text2 = action1.text, action2.text
		if pos1 > pos2:
			pos1, pos2 = pos2, pos1
			text1, text2 = text2, text1
		len1, len2 = len(text1), len(text2)
		
		intersection = (pos1+len1) - pos2
		if intersection >= 0:
			new_pos = len1 - intersection
			text3 = text1[:new_pos] + text2 + text1[new_pos:]
			print('qwe')
			return InsertAction(pos1, text3, action1.from_version, action2.to_version)
	
	if (type(action1) == type(action2) == DeleteAction):
		pos1, pos2 = action1.pos, action2.pos
		len1, len2 = action1.length, action2.length
		if pos1 > pos2:
			pos1, pos2 = pos2, pos1
			len1, len2 = len2, len1
		
		intersection = pos1+len1 - pos2
		if intersection >= 0:
			len3 = len1 + len2 - (2*intersection)
			return DeleteAction(pos1, len3, action1.from_version, action2.to_version)
		
	return action2