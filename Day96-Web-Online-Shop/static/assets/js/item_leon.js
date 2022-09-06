
<script id="cart-us" type="x-tmpl-mustache">
        <div class="cart__body">
          <div class="cart-items">
            {{>ln}}
          </div>
          <div class="cart__total">
            <h5 class="cart__total-title">Subtotal</h5><!-- /.cart__total-title -->
            <p>{{cart.subtotal.formatted_with_symbol}}</p>
          </div><!-- /.cart__total -->
          <div class="cart__items-extra">
            <div class="main-carousel splide slider-cart js-slider-cart" role="group">
              <div class="splide__track">
                <div class="splide__list">
                  {{>addonsUI}}
                </div>
              </div>
            </div><!-- /.main-carousel -->
          </div><!-- /.cart__suggested-itema -->
        </div><!-- /.cart__body -->`

        <div class="cart__foot">
          <div class="cart__actions">
            <a href="javascript:void()" onclick='Spaces.goToCheckout(this); return false;' class="button button-danger button-danger--big">Secure Checkout</a>
          </div><!-- /.cart__actions -->

          <div id="cart-offer-informations" class="cart__offer-informations is-hidden">
          </div><!-- /.cart__offer-informations-->

          <!--<p>All transactions are safe & secured<br>by 256 bit AES encryption</p>-->

          <div id="fake-product_paypal_ban--cart" class="fake-product_paypal_ban">
            <p>Pay in 4 interest-free payments with </p><img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/paypal-logo-text.svg" alt="paypal logo" loading="lazy"/>
          </div>

          <div class="payment-logos">
            <ul>
              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/Visa.svg" alt="visa logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/MasterCard.svg" alt="mastercard logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/AMEX.svg" alt="amex logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/Discover.svg" alt="discover logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/GPay.svg" alt="google pay logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/ApplePay.svg" alt="apple pay logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/PayPal.svg" alt="paypal logo" width="39" height="28">
              </li>
            </ul>
          </div>

          <p>The pictures are representative of the plants we deliver, but there may be minor differences in the size and shape of foliage.</p>
        </div><!-- /.cart__foot -->
</script>
<script id="cart-fr" type="x-tmpl-mustache">
        <div class="cart__body">
          <div class="cart-items">
            {{>ln}}
          </div>
          <div class="cart__total">
            <h5 class="cart__total-title">Subtotal</h5><!-- /.cart__total-title -->
            <p>{{cart.subtotal.formatted_with_symbol}}</p>
          </div><!-- /.cart__total -->
          <div class="cart__items-extra">
            <div class="main-carousel splide slider-cart js-slider-cart" role="group">
              <div class="splide__track">
                <div class="splide__list">
                  {{>addonsUI}}
                </div>
              </div>
            </div><!-- /.main-carousel -->
          </div><!-- /.cart__suggested-itema -->
        </div><!-- /.cart__body -->`

        <div class="cart__foot">
          <div class="cart__actions">
            <a href="javascript:void()" onclick='Spaces.goToCheckout(this); return false;' class="button button-danger button-danger--big">Secure Checkout</a>
          </div><!-- /.cart__actions -->

          <div id="cart-offer-informations" class="cart__offer-informations is-hidden">
          </div><!-- /.cart__offer-informations-->

          <!--<p>All transactions are safe & secured<br>by 256 bit AES encryption</p>-->

          <div id="fake-product_paypal_ban--cart" class="fake-product_paypal_ban">
            <p>Pay in 4 interest-free payments with </p><img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/paypal-logo-text.svg" alt="paypal logo" loading="lazy"/>
          </div>

          <div class="payment-logos">
            <ul>
              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/Visa.svg" alt="visa logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/MasterCard.svg" alt="mastercard logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/AMEX.svg" alt="amex logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/Discover.svg" alt="discover logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/GPay.svg" alt="google pay logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/ApplePay.svg" alt="apple pay logo" width="39" height="28">
              </li>

              <li>
                <img src="https://d3gkbidvk2xej.cloudfront.net/assets/images/svg/PayPal.svg" alt="paypal logo" width="39" height="28">
              </li>
            </ul>
          </div>

          <p>The pictures are representative of the plants we deliver, but there may be minor differences in the size and shape of foliage.</p>
        </div><!-- /.cart__foot -->
</script>
<script id="cart-addons" type="x-tmpl-mustache">
{{#addons}}
<div class="carousel-cell splide__slide">
  <div class="item-extra">
    <div class="item__image"  loading="lazy" style="background-image: url({{Variants.0.Options.0.Images.0.url}}&w=180);"></div><!-- /.item__image -->

    <div class="item__content">
      <div class="item__entry">
        <h6 class="item__title">{{name}}</h6><!-- /.item__title -->
        <p>{{short_description}}<br/>{{Variants.0.Options.0.name}}</p>

      </div><!-- /.item__entry -->

      <div class="item__actions">
        <p>${{Variants.0.Options.0.price}} <a
          {{#red}}
          style='color: #e46d5f'
          {{/red}}
          class='redLink'
        href="javascript:Spaces.AddToCart({product_id:'{{id}}', variant_id:'{{Variants.0.id}}', variant_option_id:'{{Variants.0.Options.0.id}}'});"
        >Add to Cart</a></p>
      </div><!-- /.item__actions -->
    </div><!-- /.item__content -->
  </div><!-- /.item-extra -->
</div>
{{/addons}}
</script>
<script id="cart-many-items" type="x-tmpl-mustache">
        {{#cart.line_items}}
          <div class="cart-item">
            <div class="cart__item-image" style="background-image: url({{image}}&w=200);"></div><!-- /.cart__item-image -->
            <div class="cart__item-content">
              <div class="cart__item-head">
                <div class="cart__item-head-inner">
                  <h6 class="cart__item-title">{{name}}</h6><!-- /.cart__item-title -->
                </div><!-- /.cart__item-head-inner -->
                <a href="javascript:void"  onclick="Spaces.removeItem('{{id}}');return false;">
                    <span class="is-hidden">remove item</span>
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M20 7V9H4V7H8V5C8 4.448 8.447 4 9 4H15C15.553 4 16 4.448 16 5V7H20ZM14 6H10V7H14V6ZM17 18V11H19V19C19 19.552 18.553 20 18 20H6C5.447 20 5 19.552 5 19V11H7V18H17Z" fill="#545454"/>
                  </svg>
                </a>
              </div><!-- /.cart__item-head -->
              <div class="cart__item-entry">
                <p>
                  {{#variants}}
                    {{option_name}}
                    {{#isABActive}}
                      {{#optionIsPreorder}}
                        <br/><small class='has-text-success'>Next batch estimated to be fulfilled <b>{{optionAvailabilitydate}}</b></small>
                      {{/optionIsPreorder}}
                      {{^optionIsPreorder}}
                        {{#availablenow}}
                          <br/><small class='has-text-success'>Available Now</small>
                        {{/availablenow}}
                        {{#highdemand}}
                          <br/><small class='has-text-success'>High Demand</small>
                        {{/highdemand}}
                        {{#fastprocessing}}
                          <br/><small class='has-text-success'>Available and Fast Processing</small>
                        {{/fastprocessing}}

                        {{#availablenowred}}
                          <br/><small class='has-text-danger'>Available Now</small>
                        {{/availablenowred}}
                        {{#highdemandred}}
                          <br/><small class='has-text-danger'>High Demand</small>
                        {{/highdemandred}}
                        {{#fastprocessingred}}
                          <br/><small class='has-text-danger'>Available and Fast Processing</small>
                        {{/fastprocessingred}}

                      {{/optionIsPreorder}}
                    {{/isABActive}}
                  {{/variants}}
                </p>
              </div><!-- /.cart__item-entry -->


              <div class="cart__item-foot">
                <div class="cart__item-actions">
                  <div class="field-number">
                      <button type="button" onclick='Spaces.quantity("{{id}}", "{{#decrementValue}}{{quantity}}{{/decrementValue}}"); return false;' class="field__btn js-field-btn js-field-decrement">
                        <span>-</span>
                      </button>

                      <label for="{{id}}" class="is-hidden">quantity</label>
                      <input type="number" id="{{id}}" value="{{quantity}}" onchange="Spaces.quantity('{{id}}', event.target.value)" class="field__input" min="1" max="100" step="1">

                      <button type="button" onclick='Spaces.quantity("{{id}}", "{{#incrementValue}}{{quantity}}{{/incrementValue}}"); return false;' class="field__btn js-field-btn js-field-increment">
                        <span>+</span>
                      </button>
                  </div><!-- /.field-number -->
                </div><!-- /.cart__item-actions -->

                <div class="cart__item-pirce">
                  <p>{{line_total.formatted_with_symbol}}</p>
                </div><!-- /.cart__item-pirce -->
              </div><!-- /.cart__item-foot -->
            </div><!-- /.cart__item-content -->
          </div><!-- /.cart-item -->
        {{/cart.line_items}}
</script>

<script id="cart-empty" type="x-tmpl-mustache">
      <div class="cart__message">
						<p>Your cart is empty!</p>
      			<a href="/products/collection/all-plants" class="button button-danger button-danger--big">Continue Shopping</a>
      </div><!-- /.cart__message -->
</script>

<script id="cart-header" type="x-tmpl-mustache">
    <p class="h4 cart__title is-active">Your Cart</p><!-- /.cart__title -->
    <p>({{count}} item{{plural}})</p>
</script>

