# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from gensim.models import word2vec
from gensim import models
import logging

def main():
	logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
	
	# model = models.Word2Vec.load_word2vec_format('wiki.zh.model.bin',binary=True)
	model = word2vec.Word2Vec.load('wiki.zh.model')

	print("提供 3 种测试模式")
	print("输入一个词，则去寻找前二十个该词的相似词")
	print("输入两个词，则去计算两个词的余弦相似度")
	print("输入三个词，进行类比推理")

	while True:
		query = raw_input("请输入: ")
		query = query #.decode('utf-8')
		q_list = query.split()
		try:
			if len(q_list) == 1:
				print("相似词前 20 排序")
				res = model.most_similar(q_list[0], topn = 20)
				for item in res:
					print(item[0]+","+str(item[1]))

			elif len(q_list) == 2:
				print("计算 Cosine 相似度")
				res = model.similarity(q_list[0], q_list[1])
				print(res)
				
			else:
				print("%s之于%s，如%s之于" % (q_list[0], q_list[2], q_list[1]))
				res = model.most_similar([q_list[0], q_list[1]], [q_list[2]], topn = 20)
				for item in res:
					print(item[0]+","+str(item[1]))
					
			print("----------------------------")
		except Exception as e:
			print(repr(e))


def utf8writer_register(): 
	import sys 
 
	if sys.platform == "win32": 
		import codecs 
		from ctypes import WINFUNCTYPE, windll, POINTER, byref, c_int 
		from ctypes.wintypes import BOOL, HANDLE, DWORD, LPWSTR, LPCWSTR, LPVOID 
 
		original_stderr = sys.stderr 
 
		# If any exception occurs in this code, we'll probably try to print it on stderr, 
		# which makes for frustrating debugging if stderr is directed to our wrapper. 
		# So be paranoid about catching errors and reporting them to original_stderr, 
		# so that we can at least see them. 
		def _complain(message): 
			print >> original_stderr, message if isinstance(message, str) else repr(message) 
 
		# Work around <http://bugs.python.org/issue6058>. 
		codecs.register(lambda name: codecs.lookup('utf-8') if name == 'cp65001' else None) 
 
		# Make Unicode console output work independently of the current code page. 
		# This also fixes <http://bugs.python.org/issue1602>. 
		# Credit to Michael Kaplan <http://blogs.msdn.com/b/michkap/archive/2010/04/07/9989346.aspx> 
		# and TZOmegaTZIOY 
		# <http://stackoverflow.com/questions/878972/windows-cmd-encoding-change-causes-python-crash/1432462#1432462>. 
		try: 
			# <http://msdn.microsoft.com/en-us/library/ms683231(VS.85).aspx> 
			# HANDLE WINAPI GetStdHandle(DWORD nStdHandle); 
			# returns INVALID_HANDLE_VALUE, NULL, or a valid handle 
			# 
			# <http://msdn.microsoft.com/en-us/library/aa364960(VS.85).aspx> 
			# DWORD WINAPI GetFileType(DWORD hFile); 
			# 
			# <http://msdn.microsoft.com/en-us/library/ms683167(VS.85).aspx> 
			# BOOL WINAPI GetConsoleMode(HANDLE hConsole, LPDWORD lpMode); 
 
			GetStdHandle = WINFUNCTYPE(HANDLE, DWORD)(("GetStdHandle", windll.kernel32)) 
			STD_INPUT_HANDLE = DWORD(-10) 
			STD_OUTPUT_HANDLE = DWORD(-11) 
			STD_ERROR_HANDLE = DWORD(-12) 
			GetFileType = WINFUNCTYPE(DWORD, DWORD)(("GetFileType", windll.kernel32)) 
			FILE_TYPE_CHAR = 0x0002 
			FILE_TYPE_REMOTE = 0x8000 
			GetConsoleMode = WINFUNCTYPE(BOOL, HANDLE, POINTER(DWORD))(("GetConsoleMode", windll.kernel32)) 
			INVALID_HANDLE_VALUE = DWORD(-1).value 
 
			def not_a_console(handle): 
				if handle == INVALID_HANDLE_VALUE or handle is None: 
					return True 
				return ((GetFileType(handle) & ~FILE_TYPE_REMOTE) != FILE_TYPE_CHAR 
						or GetConsoleMode(handle, byref(DWORD())) == 0) 
			# old_stdin_fileno = None 
			old_stdout_fileno = None 
			old_stderr_fileno = None 
			# if hasattr(sys.stdin, 'fileno'): 
			#	 old_stdin_fileno = sys.stdin.fileno() 
			if hasattr(sys.stdout, 'fileno'): 
				old_stdout_fileno = sys.stdout.fileno() 
			if hasattr(sys.stderr, 'fileno'): 
				old_stderr_fileno = sys.stderr.fileno() 
			# STDIN_FILENO = 0 
			STDOUT_FILENO = 1 
			STDERR_FILENO = 2 
			# real_stdin = (old_stdin_fileno == STDIN_FILENO) 
			real_stdout = (old_stdout_fileno == STDOUT_FILENO) 
			real_stderr = (old_stderr_fileno == STDERR_FILENO) 
 
			# if real_stdin: 
			#	 hStdin = GetStdHandle(STD_INPUT_HANDLE) 
			#	 if not_a_console(hStdin): 
			#		 real_stdin = False 
 
			if real_stdout: 
				hStdout = GetStdHandle(STD_OUTPUT_HANDLE) 
				if not_a_console(hStdout): 
					real_stdout = False 
 
			if real_stderr: 
				hStderr = GetStdHandle(STD_ERROR_HANDLE) 
				if not_a_console(hStderr): 
					real_stderr = False 
 
			if real_stdout or real_stderr: # or real_stdin 
				# BOOL WINAPI WriteConsoleW(HANDLE hOutput, LPWSTR lpBuffer, DWORD nChars, 
				#						  LPDWORD lpCharsWritten, LPVOID lpReserved); 
 
				WriteConsoleW = WINFUNCTYPE(BOOL, HANDLE, LPWSTR, DWORD, POINTER(DWORD), LPVOID)( 
					("WriteConsoleW", windll.kernel32)) 
 
				class UnicodeOutput: 
					def __init__(self, hConsole, stream, fileno, name): 
						self._hConsole = hConsole 
						self._stream = stream 
						self._fileno = fileno 
						self.closed = False 
						self.softspace = False 
						self.mode = 'w' 
						self.encoding = 'utf-8' 
						self.name = name 
						self.flush() 
 
					def isatty(self): 
						return False 
 
					def close(self): 
						# don't really close the handle, that would only cause problems 
						self.closed = True 
 
					def fileno(self): 
						return self._fileno 
 
					def flush(self): 
						if self._hConsole is None: 
							try: 
								self._stream.flush() 
							except Exception as e: 
								_complain("%s.flush: %r from %r" % (self.name, e, self._stream)) 
								raise 
 
					def write(self, text): 
						try: 
							if self._hConsole is None: 
								if isinstance(text, unicode): 
									text = text.encode('utf-8') 
								self._stream.write(text) 
							else: 
								if not isinstance(text, unicode): 
									text = str(text).decode('utf-8') 
								remaining = len(text) 
								while remaining: 
									n = DWORD(0) 
									# There is a shorter-than-documented limitation on the 
									# length of the string passed to WriteConsoleW (see 
									# <http://tahoe-lafs.org/trac/tahoe-lafs/ticket/1232>. 
									retval = WriteConsoleW(self._hConsole, text, min(remaining, 10000), byref(n), None) 
									if retval == 0 or n.value == 0: 
										raise IOError("WriteConsoleW returned %r, n.value = %r" % (retval, n.value)) 
									remaining -= n.value 
									if not remaining: 
										break 
									text = text[n.value:] 
						except Exception as e: 
							_complain("%s.write: %r" % (self.name, e)) 
							raise 
 
					def writelines(self, lines): 
						try: 
							for line in lines: 
								self.write(line) 
						except Exception as e: 
							_complain("%s.writelines: %r" % (self.name, e)) 
							raise 
 
					def read(self, n=1): 
						return unicode(self._stream.read(n), self._stream.encoding) 
 
					def readinto(self, b): 
						return unicode(self._stream.readinto(b), self._stream.encoding) 
 
					def readline(self, limit=-1): 
						return unicode(self._stream.readline(limit), self._stream.encoding) 
 
					def readlines(self, limit=-1): 
						result = [unicode(s, self._stream.encoding) for s in self._stream.readlines(limit)] 
						return result 
 
				#if real_stdin: 
					#sys.stdin = UnicodeOutput(hStdin, None, STDIN_FILENO, '<Unicode console stdin>') 
				#else: 
 
				# It is more difficult to read from hStdin than write to hStdout, 
				# cause bottom line fully work for me, 
				# I haven't implemented it with win32api(ReadConsole). 
				sys.stdin = UnicodeOutput(None, sys.stdin, sys.stdin.fileno(), '<Unicode redirected stdin>') 
 
				if real_stdout: 
					sys.stdout = UnicodeOutput(hStdout, None, STDOUT_FILENO, '<Unicode console stdout>') 
				else: 
					sys.stdout = UnicodeOutput(None, sys.stdout, old_stdout_fileno, '<Unicode redirected stdout>') 
 
				if real_stderr: 
					sys.stderr = UnicodeOutput(hStderr, None, STDERR_FILENO, '<Unicode console stderr>') 
				else: 
					sys.stderr = UnicodeOutput(None, sys.stderr, old_stderr_fileno, '<Unicode redirected stderr>') 
 
 
		except Exception as e: 
			_complain("exception %r while fixing up sys.stdout and sys.stderr" % (e,)) 
 
 
		# While we're at it, let's unmangle the command-line arguments: 
 
		# This works around <http://bugs.python.org/issue2128>. 
		GetCommandLineW = WINFUNCTYPE(LPWSTR)(("GetCommandLineW", windll.kernel32)) 
		CommandLineToArgvW = WINFUNCTYPE(POINTER(LPWSTR), LPCWSTR, POINTER(c_int))( 
			("CommandLineToArgvW", windll.shell32)) 
 
		argc = c_int(0) 
		argv_unicode = CommandLineToArgvW(GetCommandLineW(), byref(argc)) 
 
		argv = [argv_unicode[i].encode('utf-8') for i in xrange(0, argc.value)] 
 
		if not hasattr(sys, 'frozen'): 
			# If this is an executable produced by py2exe or bbfreeze, then it will 
			# have been invoked directly. Otherwise, unicode_argv[0] is the Python 
			# interpreter, so skip that. 
			argv = argv[1:] 
 
			# Also skip option arguments to the Python interpreter. 
			while len(argv) > 0: 
				arg = argv[0] 
				if not arg.startswith(u"-") or arg == u"-": 
					break 
				argv = argv[1:] 
				if arg == u'-m': 
					# sys.argv[0] should really be the absolute path of the module source, 
					# but never mind 
					break 
				if arg == u'-c': 
					argv[0] = u'-c' 
					break 
 
		# if you like: 
		sys.argv = argv 
		
		
if __name__ == "__main__":
	# 避免 windows 下中文乱码
	utf8writer_register()
	main()
