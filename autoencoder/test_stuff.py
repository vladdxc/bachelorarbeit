
import numpy as np

x = np.ones((2,2))
y = np.empty(shape=np.shape(x))
print(y)
""""
'Obsolete utility function for reading data'
def datagenerator(datadir, normalization_type, format):
    #patches_fl = os.listdir(datadir)
    patches_fl = glob.glob(datadir)
    data = np.empty((len(patches_fl), 128, 128, 2))

    for k, ids in enumerate(patches_fl):
        abs_path = ids
        if format == 'tif':
        #abs_path = datadir + ids
            ret = io.imread(abs_path)
            ret = ret.astype(np.float32)
            data[k, ] = ret

        elif format == 'mat':
            f = h5py.File(abs_path)
            ret = np.array(f['ret'])
            data[k, :, :, 0] = ret[0]
            data[k, :, :, 1] = ret[1]
        else:
            print('Please make sure files are in valid format!(mat, tif, etc)')

    if normalization_type == 'max1':
        data = np.divide(data, np.amax(data))
        return data
    else:
        return data
'Obsolete utility functions for parsing data to the TFRecord file format'
def print_progress(count, total):
    pct_complete = float(count) / total
    msg = "\r- Progress: {0:.1%}".format(pct_complete)
    sys.stdout.write(msg)
    sys.stdout.flush()


def wrap_int64(value):
    return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))


def wrap_bytes(value):
    return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))


def convert(image_paths, labels, out_path, size):
    print("Converting: " + out_path)
    image_paths = glob.glob(image_paths)
    num_images = len(image_paths)
    labels = 1
    with tf.python_io.TFRecordWriter(out_path) as wrt:
        for i, path in enumerate(image_paths):
            print_progress(count=i, total=num_images - 1)
            img = io.imread(path)
            img_bytes = img.tostring()
            data = {'image': wrap_bytes(img_bytes), 'label': wrap_int64(labels)}
            feature = tf.train.Features(feature=data)
            example = tf.train.Example(features=feature)
            serialized = example.SerializeToString()
            wrt.write(serialized)


def input_fn(out_path, shuffle=False, repeat_count=1, batch_size=1, input_name='encoder_input'):
    def _parse_function(serialized):
        features = {'image': tf.FixedLenFeature([], tf.string), 'label': tf.FixedLenFeature([], tf.int64)}
        parsed_example = tf.parse_single_example(serialized=serialized, features=features)
        image_shape = tf.stack([128, 128, 2])
        image_raw = parsed_example['image']
        label = tf.cast(parsed_example['label'], tf.float32)
        image = tf.decode_raw(image_raw, tf.uint8)
        image = tf.cast(image, tf.float32)
        image = tf.reshape(image, image_shape)
        d = dict(zip([input_name], [image])), [label]
        return d

    dataset = tf.data.TFRecordDataset(filenames=out_path)
    dataset = dataset.map(_parse_function)
    if shuffle:
        dataset = dataset.shuffle(buffer_size=256)
    dataset = dataset.repeat(repeat_count)
    dataset = dataset.batch(batch_size)
    iterator = dataset.make_one_shot_iterator()
    batch_features, batch_labels = iterator.get_next()
    return batch_features, batch_labels
"""