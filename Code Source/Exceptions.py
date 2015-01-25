

class CelluleException( Exception ):
	"""
	Se déclenche lors d'une exception dans la classe Cellule
	"""
	def __init__(self, message):
		# Call the base class constructor with the parameters it needs
		super(ValidationError, self).__init__(message)


class LienException( Exception ):
	"""
	Se déclenche lors d'une exception dans la classe Lien
	"""
	pass


class MouvementException( Exception ):
	"""
	Se déclenche lors d'une exception dans la classe Mouvement
	"""
	pass


class TerrainException( Exception ):
	"""
	Se déclenche lors d'une exception dans la classe Terrain
	"""
	pass


class RobotException( Exception ):
	"""
	Se déclenche lors d'une exception dans la classe Robot
	"""
	pass
