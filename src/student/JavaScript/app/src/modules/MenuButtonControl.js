export function createControlButton({className = 'control-button', iconClass=undefined, onClick=undefined, title=null}={}){

    // create container div
    const container = document.createElement('div');
    container.className = `mapboxgl-ctrl mapboxgl-ctrl-group ${className}`;
  
    // create button
    const button = document.createElement('button');
    button.className = 'mapboxgl-ctrl-icon';
    button.onclick = onClick;
    button.title = title;
  
    // create icon
    const icon = document.createElement('i');
    icon.className = iconClass;
  
    // return div
    button.appendChild(icon);
    container.appendChild(button);
  
    // create a new mapboxgl.IControl-like class
    class MenuButtonControl {
      // mapboxgl.IControl must implement these methods!
      onAdd(map){
        this._map = map;
        this._container = container;
        return this._container;
      }
  
      onRemove() {
        this._container.parentNode.removeChild(this._container);
        this._map = undefined;
      }
    }
  
    // return new MenuControlButton()
    return new MenuButtonControl()
  }