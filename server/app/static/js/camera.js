// <-----------------------------------------< Header >----------------------------------------->
//
//       camera.py
//       By: Fredrick Stakem
//       Date: 3.5.14
//
//
// <-----------------------------------------<---~~--->----------------------------------------->


// Libraries
// None

function Camera(name, ip_address)
{
	this.name = name;
	this.ip_address = ip_address;
	this.photos = new Array();
};

Camera.prototype = 
{	
	removePhotosWithoutPath: function()
	{
		var new_photos = new Array();

		for(i = 0; i < this.photos.length; i++)
		{
			var photo = this.photos[i];

			if(photo.path != '')
			{
				new_photos.push(photo)
			}
		}
	},

	addPhotos: function(photos)
	{
		for(i = 0; i < photos.length; i++)
		{
			var photo = photos[i];
			var add_photo = true;

			for(j = 0; j < this.photos.length; j++)
			{
				if(this.photos[j].equals(photo))
				{
					add_photo = false;
					break;
				}
			}

			if(add_photo)
			{
				this.photos[this.photos.length] = photo;
			}
		}
	}
};