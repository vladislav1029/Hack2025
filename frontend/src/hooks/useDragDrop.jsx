import { useState, useEffect, useCallback } from 'react';

// Hook for managing component drag-and-drop on dashboard pages
export const useDragDrop = (pageName, initialLayout = null) => {
  const storageKey = `dashboard_${pageName}_layout`;

  // Get saved layout from localStorage or use default
  const getSavedLayout = useCallback(() => {
    try {
      const saved = localStorage.getItem(storageKey);
      return saved ? JSON.parse(saved) : initialLayout || [];
    } catch (error) {
      console.warn('Failed to load saved layout:', error);
      return initialLayout || [];
    }
  }, [initialLayout, storageKey]);

  // Save layout to localStorage
  const saveLayout = useCallback((layout) => {
    try {
      localStorage.setItem(storageKey, JSON.stringify(layout));
    } catch (error) {
      console.warn('Failed to save layout:', error);
    }
  }, [storageKey]);

  const [layout, setLayout] = useState(getSavedLayout);
  const [isDragMode, setIsDragMode] = useState(false);
  const [draggedItem, setDraggedItem] = useState(null);

  // Save layout whenever it changes
  useEffect(() => {
    saveLayout(layout);
  }, [layout, saveLayout]);

  // Toggle drag mode
  const toggleDragMode = () => {
    setIsDragMode(prev => !prev);
    setDraggedItem(null);
  };

  // Handle drag start
  const handleDragStart = (e, itemId, itemType) => {
    if (!isDragMode) return;

    setDraggedItem({ id: itemId, type: itemType });
    e.dataTransfer.effectAllowed = 'move';
    e.target.style.opacity = '0.5';
  };

  // Handle drag end
  const handleDragEnd = (e) => {
    e.target.style.opacity = '1';
    setDraggedItem(null);
  };

  // Handle drag over
  const handleDragOver = (e) => {
    if (!isDragMode) return;
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  // Handle drop
  const handleDrop = (e, dropZoneId) => {
    if (!isDragMode || !draggedItem) return;

    e.preventDefault();

    const newLayout = [...layout];
    const draggedIndex = newLayout.findIndex(item =>
      item.id === draggedItem.id && item.type === draggedItem.type
    );

    if (draggedIndex === -1) return;

    const [draggedComponent] = newLayout.splice(draggedIndex, 1);

    // Insert at new position
    if (dropZoneId === 'end') {
      newLayout.push(draggedComponent);
    } else {
      const dropIndex = newLayout.findIndex(item =>
        item.id === dropZoneId || item.dropZoneId === dropZoneId
      );
      newLayout.splice(dropIndex, 0, draggedComponent);
    }

    setLayout(newLayout);
    setDraggedItem(null);
  };

  // Add a component to the layout
  const addComponent = (componentId, componentType, componentData = {}) => {
    const newComponent = {
      id: componentId,
      type: componentType,
      ...componentData,
      order: layout.length
    };

    setLayout(prev => [...prev, newComponent]);
  };

  // Remove a component from the layout
  const removeComponent = (componentId, componentType) => {
    setLayout(prev =>
      prev.filter(item => !(item.id === componentId && item.type === componentType))
    );
  };

  // Update component data
  const updateComponent = (componentId, componentType, newData) => {
    setLayout(prev =>
      prev.map(item =>
        item.id === componentId && item.type === componentType
          ? { ...item, ...newData }
          : item
      )
    );
  };

  // Reset layout to default
  const resetLayout = () => {
    setLayout(initialLayout || []);
    localStorage.removeItem(storageKey);
  };

  return {
    layout,
    isDragMode,
    draggedItem,
    toggleDragMode,
    handleDragStart,
    handleDragEnd,
    handleDragOver,
    handleDrop,
    addComponent,
    removeComponent,
    updateComponent,
    resetLayout,
    saveLayout,
    getSavedLayout
  };
};
