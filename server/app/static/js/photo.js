// <-----------------------------------------< Header >----------------------------------------->
//
//       photo.py
//       By: Fredrick Stakem
//       Date: 3.7.14
//
//
// <-----------------------------------------<---~~--->----------------------------------------->


// Libraries
// None

function Photo(name, path)
{
	this.name = name;
	this.path = path;
};

Photo.prototype = 
{
	equals: function(other_photo)
	{
		if(this.name == other_photo.name && this.path == other_photo.path)
		{
			return true;
		}

		return false;
	}
};