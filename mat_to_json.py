import mat4py, json, os

gt_mat = mat4py.loadmat('caltech/gt.mat')['gt']
img_root_dir = 'caltech/train10x/images'
sets = 6
vid = [15, 6, 12, 13, 12, 13]
im_id = 0
anno_id = 0
json_im, json_anno = [], []
for i in range(sets):
    set_name = 'set' + str(i).zfill(2)
    for j in range(vid[i]):
        vid_name = 'V' + str(j).zfill(3)
        img_dir = os.path.join(img_root_dir, set_name, vid_name)
        im_list = os.listdir(img_dir)
        im_num = len(im_list)
        for k in range(2, 3 * im_num + 2, 3):
            img_name = 'I' + str(k).zfill(5)
            img_name = set_name + '_' + vid_name + '_' + img_name + '.jpg'
            im = {}
            im[u'id'] = im_id
            im[u'set_name'] = str(set_name)
            im[u'vid_name'] = str(vid_name)
            im[u'file_name'] = str(img_name)
            im[u'height'] = 480
            im[u'width'] = 640
            json_im.append(im)
            gts = gt_mat[im_id]
            if len(gts) > 0:
                if not isinstance(gts[0], list):
                    gts = [gts]
                for gt in gts:
                    [x, y, w, h, ig] = gt
                    anno = {}
                    anno[u'ignore'] = int(ig)
                    anno[u'area'] = w * h
                    anno[u'bbox'] = [x, y, w, h]
                    anno[u'category_id'] = 1
                    anno[u'id'] = anno_id
                    anno[u'image_id'] = im_id
                    anno_id = anno_id + 1
                    json_anno.append(anno)
            im_id += 1
anno_json = {}
anno_json[u'images'] = json_im
anno_json[u'annotations'] = json_anno
categories = []
category = {}
category[u'id'] = 1
category[u'name'] = 'pedestrian'
categories.append(category)
anno_json[u'categories'] = categories
json.dump(anno_json, open('caltech/train.json', 'w'))
