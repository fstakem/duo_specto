// <-----------------------------------------< Header >----------------------------------------->
//
//       camera.py
//       By: Fredrick Stakem
//       Date: 3.5.15
//
//
// <-----------------------------------------<---~~--->----------------------------------------->


var PiIot = PiIot || {};

PiIot.Camera = function(id, name, ip_address)
{
	this.id = id;
	this.name = name;
	this.ip_address = ip_address;
	this.photos = new Array();
};

PiIot.Camera.prototype = 
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

	photoIndex: function(photo)
	{
		for(i = 0; i < this.photos.length; i++)
		{
			var next_photo = this.photos[i];
			if(_.isEqual(next_photo, photo))
			{
				return i;
			}
		}

		return -1;
	},

	addPhoto: function(photo)
	{
		if(this.photoIndex(photo) < 0)
		{
			this.photos.push(photo);
		}
	},

	deletePhoto: function(photo)
	{
		var index = this.photoIndex(photo);
		if(index > 0)
		{
			this.photos.splice(index, 1);
		}
	},

	getPhotoPaths: function()
	{
		var imgs = Array();

		if(this.photos.length > 0)
		{
			for(i = 0; i < this.photos.length; i++)
		    {
		        imgs.push( { img: this.photos[i].path } )
		    }
		}
		else
		{
			imgs.push( { img: '/static/imgs/no_img.png' } )
		}

	    

	    return imgs;
	},

};