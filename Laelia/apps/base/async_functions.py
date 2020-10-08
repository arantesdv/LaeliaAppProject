import asyncio
import concurrent.futures
import time

class AsyncFunc:
	

	@staticmethod
	async def create_new_relation(patient=None, professional=None):
		print(f'Started at {time.strftime("%X")}')
		await asyncio.sleep(5)
		print(f'Finished at {time.strftime("%X")}')
	
	@staticmethod
	def blocking_io():
		# File operations (such as logging) can block the
		# event loop: run them in a thread pool.
		with open('/dev/urandom', 'rb') as f:
			return f.read(100)
	
	@staticmethod
	def cpu_bound():
		# CPU-bound operations will block the event loop:
		# in general it is preferable to run them in a
		# process pool.
		with open('/dev/urandom', 'rb') as f:
			return f.read(100)
		
	@staticmethod
	async def classRun():
		loop = asyncio.get_running_loop()
		
		## Options:
		
		# 1. Run in the default loop's executor:
		result = await loop.run_in_executor(
			None, AsyncFunc.blocking_io)
		print('default thread pool', result)
		
		# 2. Run in a custom thread pool:
		with concurrent.futures.ThreadPoolExecutor() as pool:
			result = await loop.run_in_executor(
				pool, AsyncFunc.blocking_io)
			print('custom thread pool', result)
		
		# 3. Run in a custom process pool:
		with concurrent.futures.ProcessPoolExecutor() as pool:
			result = await loop.run_in_executor(
				pool, AsyncFunc.cpu_bound)
			print('custom process pool', result)
		



if __name__ == '__main__':
	#asyncio.run(AsyncFunc.create_new_relation())
	asyncio.run(AsyncFunc.classRun())
