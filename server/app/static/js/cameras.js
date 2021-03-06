// <-----------------------------------------< Header >----------------------------------------->
//
//       cameras.py
//       By: Fredrick Stakem
//       Date: 3.28.15
//
//
// <-----------------------------------------<---~~--->----------------------------------------->


console.log('Starting javascript execution on page.')

var $fotorama_div = $('.fotorama-div').fotorama(
{
    height: 600,
    width: 800,
    arrows: true,
    nav: "thumbs",
    arrows: false,
    keyboard: false,
    data: [
          {img: 'static/imgs/pi_cover_1.png', thumb: '#'},
          {img: 'static/imgs/pi_cover_2.png', thumb: '#'}
        ]
});

var fotorama = $fotorama_div.data('fotorama');
var camera_tree = null;
var selected_camera = null;
var selected_photo = null;
var system_busy = false;
var capture_photo_url = "/capture_photo";
var fetch_photo_url = "/fetch_photo";
var search_camera_url = "/search_camera";
var delete_photos_url = "/delete_photos";
var delete_photo_url = "/delete_photo";

var test_cameras = null;

jQuery(document).ready(function () 
{
    console.log('Document ready running jQuery commands.');

    $(".ajax-button").click(function(e)
    {
        console.log("Take photos button clicked: performing AJAX");
        console.log("Camera address: " + $("#camera-address-txt").val())

        var url = '';
        var data = '';

        if(this.id == 'take-photos-button')
        {
            url = capture_photo_url;
            var cameras = getCamerasFromTree();
            data = { 'cameras': cameras }
            data = JSON.stringify(data, null, '\t');
        }
        else if(this.id == 'fetch-photos-button')
        {
            url = fetch_photo_url;
            var cameras = getCamerasFromTree();
            data = { 'cameras': cameras }
            data = JSON.stringify(data, null, '\t');
        }
        else if(this.id == 'camera-search-button')
        {
            url = search_camera_url;
            data = JSON.stringify($("#camera-address-txt").val(), null, '\t');
        }

        activateButtonSpinner(this);
        system_busy = true;
        e.preventDefault();

        $.ajax(
        {
            type: "POST",
            url: url,
            data: data,
            contentType: 'application/json;charset=UTF-8',
            success: function(raw_data, text_status, xhr)
            {
                console.log("AJAX Request success -> ", xhr, " -> ", text_status)
                deactivateButtonSpinner(this);

                if(this.url == capture_photo_url)
                {
                    takePhotosResult(raw_data, this)
                }
                else if(this.url == fetch_photo_url)
                {
                    fetchPhotosResult(raw_data, this)
                }
                else if(this.url == search_camera_url)
                {
                    searchCameraResult(raw_data, this);
                }

                system_busy = false;

            },
            complete : function(xhr, text_status) 
            {
                console.log("AJAX Request complete -> ", xhr, " -> ", text_status)
                system_busy = false
            },
            error: function(xhr, text_status, error_thrown)
            {
                console.log("AJAX Request error -> ", xhr, " -> ", text_status, " error -> ", error_thrown)
                system_busy = false;
                deactivateButtonSpinner(this);
            }
        });
    });

    $(document).bind('keydown', 'right', function(e) 
    {
        console.log('RIGHT');

        return false;
    });

    $(document).bind('keydown', 'left', function(e) 
    {
        console.log('LEFT');
        
        return false;
    });

    $('#jstree_demo_div').on('keydown.jstree', '.jstree-anchor', function (e) 
    {
        e.preventDefault();
        var instance = $.jstree.reference(this); // this is the node (as you described)
        var selected = instance.get_selected();  // array of selected nodes, you might need [0]
    })

    function activateButtonSpinner(button)
    {
        var spin = $( button ).find( ".spinner" );
        spin.toggleClass('active');

        var icon = $( button ).find( ".glyphicon.glyphicon-refresh" );
        animateClass = "glyphicon-refresh-animate";
        icon.addClass( animateClass );

        // Disable all ajax buttons
        $( ".ajax-button" ).attr('disabled', "disabled")
    }

    function deactivateButtonSpinner(ajax)
    {
        var button =  '';

        if(ajax.url == capture_photo_url)
        {
            button = $( "#take-photos-button" );
        }
        else if(ajax.url == fetch_photo_url)
        {
            button = $( "#fetch-photos-button" );
        }
        else if(ajax.url == search_camera_url)
        {
            button = $( "#camera-search-button" );
        }

        var spin = $( button ).find( ".spinner" );
        spin.toggleClass('active');
        var icon = $( button ).find( ".glyphicon.glyphicon-refresh" );
        animateClass = "glyphicon-refresh-animate";
        icon.removeClass( animateClass );

        // Enable all ajax buttons
        $( ".ajax-button" ).removeAttr('disabled', "disabled")
    }

    function getCamerasFromTree()
    {
        var cameras = new Array();

        if(camera_tree != null)
        {
            for(i = 0; i < camera_tree.core.data.length; i++)
            {
                var node = camera_tree.core.data[i];

                if(node.data instanceof PiIot.Camera)
                {
                    cameras.push(node.data);
                }
            }
        }
        
        return cameras;
    }

    function searchCameraResult(response, ajax)
    {
        var cameras = getCamerasFromTree();
        var result = ajax.data.slice(1, -1);

        if(response == 'found')
        {
            cameras[cameras.length] = new PiIot.Camera(-1, result, result);
            handleNewTreeData(cameras);
        }
        else if(response == 'not_found')
        {
            // No camera dialog
        }
    }

    function takePhotosResult(response, ajax)
    {
        var cameras = getCamerasFromTree();
        var failed_cameras = new Array();
        var response_data = JSON.parse(response);
        
        for(i = 0; i < cameras.length; i++)
        {
            var camera = cameras[i];
            var camera_response = response_data[camera.ip_address]

            if(camera_response.sucess == true)
            {
                camera.addPhotos(new PiIot.Photos(-1, '-On Client-', ''));
            }
            else
            {
                failed_cameras.push(camera);
            }
        }

        if(cameras.length > failed_cameras.length)
        {   
            handleNewTreeData(cameras);
        }

        if(failed_cameras.length > 0)
        {
            // Capture failure dialog
        }
    }

    function fetchPhotosResult(response, ajax)
    {
        var cameras = getCamerasFromTree();
        response_data = JSON.parse(response);

        for(i = 0; i < cameras.length; i++)
        {
            var camera = cameras[i];
            var camera_response = response_data[camera.ip_address]

            for(j = 0; j < camera_response.camera.imgs.length; j++)
            {
                var name = camera_response.camera.imgs[j].name;
                var path = camera_response.camera.imgs[j].url;
                var photo =  new PiIot.Photo(-1, name , path);
                
                if(camera.photoIndex(photo) < 0)
                {
                    camera.addPhoto(photo);
                }
            }
        }

        handleNewTreeData(cameras);
    }

    function handleNewTreeData(cameras)
    {
        console.log("Handle new tree data:");
        console.log(cameras);

        var no_camera_line = $('#no-cameras-p');
        if(no_camera_line.length != 0)
        {
            no_camera_line.remove();
        }
        else
        {
            $('#jstree_demo_div').jstree("destroy");
        }
        
        var data = createTree(cameras);
        camera_tree = { 
                        core: 
                        { 
                            data: data 
                        },
                        plugins: ["contextmenu"],
                        contextmenu: {items: customMenu}
                    };

        $('#jstree_demo_div').jstree(camera_tree);

        $("#jstree_demo_div").bind("select_node.jstree", function(evt, eventData)
        {
            var selectedObject = eventData.node.data;
            var parentId = eventData.node.parent;
            var parentObjectSearch = $.grep(camera_tree.core.data, function(e){return e.id == parentId;});
            var parentObject;

            if(parentObjectSearch.length > 0)
            {
                parentObject = parentObjectSearch[0].data;
            }

            if(parentObject == undefined)
            {
                var camera = new PiIot.Camera(selectedObject.id, selectedObject.name, selectedObject.ip_address);
                camera.photos = selectedObject.photos;
                selectCamera(camera);
            }
            else
            {
                var camera = new PiIot.Camera(parentObject.id, parentObject.name, parentObject.ip_address);
                camera.photos = parentObject.photos;
                var photo = new PiIot.Photo(selectedObject.id, selectedObject.name, selectedObject.path)
                selectPhoto(camera, photo);
            }
        });
    }

    function renameCamera(node)
    {

    }

    function takePhoto(node)
    {
        console.log('TAKE PHOTO');
        console.log(node.item.camera)
    }

    function fetchPhotos(node)
    {
        console.log('FETCH PHOTOS');
        console.log(node.item.camera)
    }   

    function deleteCamera(node)
    {
        console.log('DELETE CAMERA');
        console.log(node.item.camera);
    }

    function testConnectivity(node)
    {
        console.log('TEST CONNECTIVITY');
        console.log(node.item.camera)
    }

    function renamePhoto(node)
    {
        console.log(node.item.photo)
    }

    function deletePhoto(node)
    {
        var url = '';
        var data = { 
                    'camera': node.item.camera,
                    'photo': node.item.photo
                    }
        data = JSON.stringify(data, null, '\t');

        $( ".ajax-button" ).attr('disabled', "disabled")

        system_busy = true;

        $.ajax(
        {
            type: "POST",
            url: url,
            data: data,
            contentType: 'application/json;charset=UTF-8',
            success: function(raw_data, text_status, xhr)
            {
                console.log("AJAX Request success -> ", xhr, " -> ", text_status)
                $( ".ajax-button" ).removeAttr('disabled', "disabled")
                system_busy = false;

            },
            complete : function(xhr, text_status) 
            {
                console.log("AJAX Request complete -> ", xhr, " -> ", text_status)
                $( ".ajax-button" ).removeAttr('disabled', "disabled")
                system_busy = false;
            },
            error: function(xhr, text_status, error_thrown)
            {
                console.log("AJAX Request error -> ", xhr, " -> ", text_status, " error -> ", error_thrown)
                $( ".ajax-button" ).removeAttr('disabled', "disabled")
                system_busy = false;
            }
        });
    }

    function performAnalysis(node)
    {
        var path = node.item.photo.path;
        window.location.href = '/analysis?path=' + path
    }

    function customMenu(node)
    {
        var parentId = node.parent;
        var parentObjectSearch = $.grep(camera_tree.core.data, function(e){return e.id == parentId;});
        console.log(node)

        var camera = null;
        var photo = null;

        if(parentId == '#') 
        {
            camera = new PiIot.Camera(node.data.id, node.data.name, node.data.ip_address);
        }
        else
        {
            camera = parentObjectSearch[0].data;
            photo =  new PiIot.Photo(node.data.id, node.data.name , node.data.path);
        }

        var items = 
        {
            renameCamera:
            {
                label: "Rename Camera",
                action: renameCamera,
                icon: "fa fa-edit",
                camera: camera
            },
            takePhoto: 
            {
                label: "Take Photo",
                action: takePhoto,
                icon: "fa fa-camera",
                camera: camera
            },
            fetchPhotos: 
            {
                label: "Fetch Photos",
                action: fetchPhotos,
                icon: 'fa fa-download',
                camera: camera
            },
            deleteCamera: 
            {
                label: "Delete Camera",
                action: deleteCamera,
                icon: 'fa fa-remove',
                camera: camera
            },
            testConnectivity: 
            {
                label: "Test Connectivity",
                action: testConnectivity,
                icon: 'fa fa-heartbeat',
                camera: camera
            },
            renamePhoto:
            {
                label: "Rename Photo",
                action: renamePhoto,
                icon: 'fa fa-edit',
                camera: camera,
                photo: photo
            },
            deletePhoto:
            {
                label: "Delete Photo",
                action: deletePhoto,
                icon: 'fa fa-remove',
                camera: camera,
                photo: photo
            },
            performAnalysis: 
            {
                label: "Perform Analaysis",
                action: performAnalysis,
                icon: 'fa fa-image',
                camera: camera,
                photo: photo
            }
        };

        if(parentId == '#') 
        {
            delete items.renamePhoto;
            delete items.deletePhoto;
            delete items.performAnalysis;
        }
        else
        {
            delete items.renameCamera;
            delete items.takePhoto;
            delete items.fetchPhotos;
            delete items.deleteCamera;
            delete items.testConnectivity;
        }

        return items;
    }

    function createTree(cameras)
    {
        var data = []

        for(i = 0; i < cameras.length; i++)
        {
            var camera = cameras[i];
            camera.id = 'camera' + (i+1)
            var camera_node = createCameraNode(camera)
            data.push(camera_node)

            for(j =0; j < camera.photos.length; j++)
            {
                var photo = cameras[i].photos[j];
                photo.id = camera.id + "_photo" + (j+1)
                var photo_node = createPhotoNode(camera, photo)
                data.push(photo_node)
            }
        }

        return data;
    }
    
    function createCameraNode(camera)
    {
        var data = []
        data = { 'id': camera.id, 
                 'parent': '#', 
                 'text': camera.name, 
                 'icon' : 'glyphicon glyphicon-camera', 
                 'data': camera 
                };

        return data
    }

    function createPhotoNode(camera, photo)
    {
        var data = []
        data = { 'id': photo.id, 
                 'parent': camera.id, 
                 'text': photo.name, 
                 'icon' : 'glyphicon glyphicon-picture', 
                 'data': photo
                };

        return data
    }

    // Main user interaction logic => selectCamera() & selectPhoto()
    // The user has selected a camera from the camera tree
    function selectCamera(camera)
    {
        // Previously camera or nothing was selected
        if(selected_photo == null)
        {
            // Previous camera was different than current camera selected
            if(!_.isEqual(selected_camera, camera))
            {
                var imgs = camera.getPhotoPaths();
                fotorama.load(imgs);
            }
        }
        // Previously photo was selected
        else
        {
            // Previous photo selected was from different camera
            if(!_.isEqual(selected_camera, camera))
            {
                var imgs = camera.getPhotoPaths();
                fotorama.load(imgs);
            }

            fotorama.show(0);
        }

        // Set the selected items for next interaction
        selected_camera = camera;
        selected_photo = null;
    }

    // Main user interaction logic => selectCamera() & selectPhoto()
    // The user has selected a photo from the camera tree or photo roll
    function selectPhoto(camera, photo)
    {
        // Previously camera or nothing was selected
        if(selected_photo == null)
        {
            // Previous camera was different than current camera selected
            if(!_.isEqual(selected_camera, camera))
            {
                var imgs = camera.getPhotoPaths();
                fotorama.load(imgs);
            }
                
            var index = camera.photoIndex(photo);
            fotorama.show(index);
        }
        // Previously photo was selected
        else
        {
            // Previous photo selected was from different camera
            if(!_.isEqual(selected_camera, camera))
            {
                var imgs = camera.getPhotoPaths();
                fotorama.load(imgs);
            }
            
            // Previous photo selected was not the same as the current photo selected
            if(!_.isEqual(selected_photo, photo))
            {
                var index = camera.photoIndex(photo);
                fotorama.show(index);
            }
        }

        selected_camera = camera;
        selected_photo = photo;
    }

    // Menu item
    $('#camera_menu_item').addClass('active');

});



