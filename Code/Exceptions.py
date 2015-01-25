

class CelluleException( Exception ):

	def __init__(self, message):
		# Call the base class constructor with the parameters it needs
		super(ValidationError, self).__init__(message)


class LienException( Exception ):
	pass


class MouvementException( Exception ):
	pass


class TerrainException( Exception ):
	pass


class RobotException( Exception ):
	pass
