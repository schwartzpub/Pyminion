import errno

def send_data (self, client, data):
	message = str(data)
	try:
		return client.send(message)

	except socket.error, e:
		if e.errno == errno.EPIPE:
			for player in self.roster:
				if player.playerConn == client:
					[self.send_data(c, player.playerName + " has been disconnected and removed from the game. (Broken Pipe)\n") for c in (u.playerConn for u in self.roster if u.playerConn != client )]
					print player.playerName + " has quit mid-game. (Broken Pipe)"
					self.roster.remove(player)
					time.sleep(2)
		else:
			clients.remove(client)
			for player in self.roster:
				if player.playerConn == client:
					[self.send_data(c, player.playerName + " has been disconnected and removed from the game. (Connection Reset by Peer)\n") for c in (u.playerConn for u in self.roster if u.playerConn != client )]
					print player.playerName + " has quit. (Connection Reset By peer)"
					self.roster.remove(player)
					time.sleep(2)

def recv_data (self, client, length):
	try:
		self.playerConn.settimeout(600)
		data = client.recv(length)
		self.playerConn.settimeout(None)
		if not data: self.send_data(self.playerConn, "Please choose an option...\n")
		return data

	except socket.timeout:
		for user in self.roster:
			if user.playerConn != self.playerConn:
				self.send_data(user.playerConn, self.playerName + " is taking a bit to respond...be patient.\n")
	except socket.error, e:
		if e.errno == errno.EPIPE:
			for player in self.roster:
				if player.playerConn == client:
					[self.send_data(c, player.playerName + " has been disconnected and removed from the game. (Broken Pipe)\n") for c in (u.playerConn for u in self.roster if u.playerConn != client )]
					print player.playerName + " has quit mid-game. (Broken Pipe)"
					self.roster.remove(player)
					self.game.playerRost.remove(player)
					time.sleep(2)
		else:
			clients.remove(client)
			for player in self.roster:
				if player.playerConn == client:
					[self.send_data(c, player.playerName + " has been disconnected and removed from the game. (Connection Reset by Peer)\n") for c in (u.playerConn for u in self.roster if u.playerConn != client )]
					print player.playerName + " has quit. (Connection Reset By peer)"
					self.roster.remove(player)
					self.game.playerRost.remove(player)
					time.sleep(2)
