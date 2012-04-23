    def chair_move(self,chair,player):
        
        # chair on chair? haha...too long coding
    
        
        chair.detect_court_collisions()
        player.detect_court_collisions()
        
        dx = 0
        dy = 0

        # move player unless colliding with court
    
        if chair.__class__.__name__ == 'Chair' and player.__class__.__name__ == 'Player':
            self.player.touching_chair = True
        else:
            self.player.touching_chair = False
    
    
        if player.__class__.__name__ == 'Chair':  # if its two chairs hitting each other
            
            # chair on chair comes up while player is touching bottom of other chair :(
            '''
            if self.player_key_list[K_w] is 1:
                chair.hit_other_chair_bottom = True
            else:
                chair.hit_other_chair_bottom = False
            
            if self.player_key_list[K_s] is 1:
                chair.hit_other_chair_top = True
            else:
                chair.hit_other_chair_top = False
            
            if self.player_key_list[K_d] is 1:
                chair.hit_other_chair_left = True
            else:
                chair.hit_other_chair_left = False
            
            if self.player_key_list[K_a] is 1:
                chair.hit_other_chair_right = True
            else:
                chair.hit_other_chair_right = False
            '''
            
        if not chair.hit_top_bound and not chair.hit_bottom_bound and not chair.hit_left_bound and not chair.hit_right_bound:
            if self.player_key_list[K_w] is 1 and (not chair.hit_top_bound or player.hit_top_bound) and self.player.touching_chair:
                    dy=-1
            if self.player_key_list[K_s] is 1 and not player.hit_bottom_bound:
                    dy  = 1
            if self.player_key_list[K_a] is 1 and not player.hit_left_bound:                 
                    dx  = -1
                    if self.player.touching_chair:
                        self.player.rect.left += 1
            if self.player_key_list[K_d] is 1 and not player.hit_right_bound:
                dx = 1
                if self.player.touching_chair:
                    self.player.rect.left -= 1
                
            chair.rect.left += dx
            chair.rect.top += dy
            chair.position = array([chair.rect.left,chair.rect.top])
            
            
            

    def chair_boundry_move (self,chair):
        if chair.hit_top_bound:
            # allow side to side movement of chair
            if self.player_key_list [K_d] is 1:
                chair.rect.left += 1
            elif self.player_key_list[K_a] is 1:
                chair.rect.left -= 1
            elif self.player_key_list[K_w] is 1:
                self.player.rect.top += 1 # cancel out movement against chair
        elif chair.hit_bottom_bound:
            if self.player_key_list [K_d] is 1:
                chair.rect.left -= 1
            elif self.player_key_list[K_a] is 1:
                chair.rect.left -= 1
            elif self.player_key_list[K_s] is 1:
                self.player.rect.top -= 1
        elif chair.hit_left_bound:
            
            chi = ((chair.rect.top - 251) / 421.0)
            x = (chi * -205.0) + 223.0  # linear interpolation
            y = -2.05 * x + 708.9  # linear formula
            
            
            if self.player_key_list [K_w] is 1:
                chair.rect.left = x + 1
                chair.rect.top = y - 1
            elif self.player_key_list[K_a] is 1:
                self.player.rect.left += 1
            elif self.player_key_list[K_s] is 1:
                chair.rect.left = x - 1
                chair.rect.top = y + 1
            
            
        elif chair.hit_right_bound:
            chi = ((chair.rect.top - 251) / 421.0)
            x = (chi * 213.0) + 899.0  # linear interpolation
            y = 1.98 * x - 1529.76  # linear formula
            
            if self.player_key_list [K_d] is 1:
                self.player.rect.left += -1
            elif self.player_key_list[K_w] is 1:
                chair.rect.top = y - 1
                chair.rect.left = x - 1
            elif self.player_key_list[K_s] is 1:
                chair.rect.top = y + 1
                chair.rect.left = x + 1
                
  def detect_court_collisions(self):
                # [223,251]      [899 251]
        #
        #    Basketball Court
        #
        # [18 672]       [1112 672]
        # Linear interpolation of left side of court (Player bounding)
        # Thanks to Jeff Sullivan!!
        
        chi = ((self.rect.top - 251) / 421.0)
        self.bounding_x_left = (chi * -205.0) + 223.0
            
            # Left Court
        if self.rect.left <= math.ceil(self.bounding_x_left) and self.rect.left >= math.floor(self.bounding_x_left):
            self.hit_left_bound = True
            print "Left Hit!"
        else:
        chi = ((self.rect.top - 251) / 421.0)
        self.bounding_x_right = (chi * 213.0) + 899.0   
        # Right Court
        if self.rect.left <= math.ceil(self.bounding_x_right) and self.rect.left >= math.floor(self.bounding_x_right):
            self.hit_right_bound = True
            print "Right Hit!"
        else:
            self.hit_right_bound = False
        
        # Bottom Court
        
        if self.rect.top >= 671 and self.rect.top <= 673:
            print "Hit Bottom"
            self.hit_bottom_bound = True
        else:
            self.hit_bottom_bound = False
        
        #Top Court
        if self.rect.top >= 250 and self.rect.top <= 252:
            print "Hit Top"
            self.hit_top_bound = True
        else:
            self.hit_top_bound = False 
    
	def get_full_hitmask(self, image, rect):
		"""returns a completely full hitmask that fits the image,
		without referencing the images colorkey or alpha."""
		mask=[]
		for x in range(rect.width):
			mask.append([])
			for y in range(rect.height):
				mask[x].append(True)
		return mask
  

