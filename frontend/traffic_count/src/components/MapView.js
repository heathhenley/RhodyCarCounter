import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import Image from 'react-bootstrap/Image';
import { cameraNameToAWSLink } from '../utils/utils';

const CameraMarker = ({ camera }) => {
  if (!camera.latitude || !camera.longitude) return null;

  return (  
    <Marker position={[camera.latitude, camera.longitude]}>
      <Popup maxWidth={350}>
        <h3>{camera.name}</h3>
        <p>{camera.description}</p>
        <Image
          src={cameraNameToAWSLink(camera.name)}
          alt={camera.description}
          width="350" />
      </Popup>
    </Marker>
  );
}


const MapView = ({ cameras }) => {
  let position = [41.82567266252603, -71.41127087426186];

  return (
    <div className="MapView">
      <MapContainer center={position} zoom={13} style={{ height: "90vh" }}>
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {cameras ? cameras.map((c) => <CameraMarker key={c.id} camera={c} />) : null}
      </MapContainer>
    </div>
  );
}

export default MapView;